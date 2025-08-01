from datetime import datetime

from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from src.config import settings
from src.db.session import get_db
from src.handlers.camera_handler import CameraHandler
from src.handlers.country_fix_handler import CountryFixHandler
from src.handlers.database_handler import DatabaseHandler
from src.handlers.plate_recognizer_handler import PlateRecognizerHandler
from src.logger import logger
from src.schemas.vehicle_detection_request import VehicleDetectionRequest

app = FastAPI()
camera_service = CameraHandler()
plate_service = PlateRecognizerHandler()
db_handler = DatabaseHandler()
country_fix_handler = CountryFixHandler()

basic_auth = HTTPBasic()


@app.post("/api/vehicle_detected")
async def handle_vehicle_detection(
    request: VehicleDetectionRequest,
    background_tasks: BackgroundTasks,
    credentials: HTTPBasicCredentials = Depends(basic_auth),
):
    # Auth check (keep this synchronous for security)
    if (
        credentials.username != settings.synology_username
        or credentials.password != settings.synology_password
    ):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    logger.info(f"Vehicle detected from camera: {request.camera}")

    detection_time = datetime.now()
    timestamp_str = detection_time.strftime("%Y%m%d_%H%M%S")

    # Add the processing to background tasks
    background_tasks.add_task(
        process_vehicle_detection,
        request.camera,
        detection_time,
        # Note: Can't pass db session to background task, need to create new one
    )

    # Return immediately
    return {"status": "accepted", "timestamp": timestamp_str}


def process_vehicle_detection(camera_name: str, detection_time: datetime):
    """Background processing function"""
    try:
        with get_db() as db:
            # Your existing processing logic here
            sid = camera_service.authenticate_client(
                host=settings.synology_host,
                username=settings.synology_username,
                password=settings.synology_password,
            )

            cameras = camera_service.get_camera_data(
                host=settings.synology_host, sid=sid
            )
            if not cameras:
                logger.error("No cameras found")
                return

            target_camera = None
            for camera in cameras:
                if camera.name == camera_name:
                    target_camera = camera
                    break

            if not target_camera:
                logger.error(f"Camera '{camera_name}' not found.")
                return

            frame = camera_service.get_camera_snapshot(
                host=settings.synology_host, sid=sid, camera=target_camera
            )

            if not frame:
                logger.error("Failed to get snapshot")
                return

            image_data = frame.content
            result = plate_service.send_to_api(image_data=image_data)
            if not result:
                logger.error("Failed to get reader results")
                return

            logger.debug(f"Plate Recognizer results: {result}")

            observations_to_create = db_handler.new_observation(
                reader_result=result, detection_timestamp=detection_time
            )

            for observation_data in observations_to_create:
                if observation_data.country_code == "unknown":
                    observation_data = country_fix_handler.fix_slovenian_plates(
                        observation=observation_data
                    )

                observation_data = db_handler.hash_plate(observation=observation_data)

                if not db_handler.check_for_duplicates(
                    db=db,
                    observation=observation_data,
                    current_detection_time=detection_time,
                ):
                    db_handler.create_observation_entry(
                        db=db, observation=observation_data
                    )
                else:
                    logger.info(
                        f"Duplicate observation for plate hash {observation_data.plate_hash.hex()} within one minute of detection. Skipping."
                    )

    except Exception as e:
        logger.exception(f"Background processing error: {e}")

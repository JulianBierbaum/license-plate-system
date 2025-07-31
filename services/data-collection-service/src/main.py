from datetime import datetime

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from src.config import settings
from src.db.session import SessionDep
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
    db: SessionDep,
    credentials: HTTPBasicCredentials = Depends(basic_auth),
):
    """Webhook for handling new vehicle detections from an ip camera

    Args:
        request (VehicleDetectionRequest): request body with the name of the camera
        db (SessionDep): db session
        credentials (HTTPBasicCredentials, optional): http basic auth credentials. Defaults to Depends(basic_auth).

    Raises:
        HTTPException: 401 raised if wrong creds
        Exception: raised if the camera data list is empty
        Exception: raised if a camera with a specified id is not in the data list
        Exception: raised if the snapshot collection failed
        HTTPException: 400 raised for basic client errors

    Returns:
        _type_: _description_
    """
    if (
        credentials.username != settings.synology_username
        or credentials.password != settings.synology_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
        )

    logger.info(f"Vehicle detected from camera: {request.camera}")

    detection_time = datetime.now()
    timestamp_str = detection_time.strftime("%Y%m%d_%H%M%S")

    try:
        sid = camera_service.authenticate_client(
            host=settings.synology_host,
            username=settings.synology_username,
            password=settings.synology_password,
        )

        cameras = camera_service.get_camera_data(host=settings.synology_host, sid=sid)
        if not cameras:
            raise Exception("No cameras found")

        target_camera = None
        for camera in cameras:
            if camera.name == request.camera:
                target_camera = camera
                break

        if not target_camera:
            raise Exception(f"Camera '{request.camera}' not found.")

        frame = camera_service.get_camera_snapshot(
            host=settings.synology_host, sid=sid, camera=target_camera
        )

        if not frame:
            raise Exception("Failed to get snapshot")

        image_data = frame.content

        # Process image with plate recognition
        result = plate_service.send_to_api(image_data=image_data)
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
                db_handler.create_observation_entry(db=db, observation=observation_data)
            else:
                logger.info(
                    f"Duplicate observation for plate hash {observation_data.plate_hash.hex()} within one minute of detection. Skipping."
                )

        return {"status": "ok", "timestamp": timestamp_str, "result": result}
    except Exception as e:
        logger.exception(f"Error: {e}")
        raise HTTPException(
            status_code=400,
            detail=f"Error: {str(e)}",
        )

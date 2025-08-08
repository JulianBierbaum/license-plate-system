import os
from datetime import datetime, timedelta

from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from src.config import settings
from src.db.session import get_db
from src.exceptions.camera_exceptions import (
    AuthenticationError,
    CameraDataError,
    SnapshotError,
)
from src.exceptions.database_exceptions import (
    DatabaseIntegrityError,
    DatabaseQueryError,
)
from src.exceptions.plate_recognizer_exceptions import PlateRecognizerCallError
from src.handlers.camera_handler import CameraHandler
from src.handlers.country_handler import CountryHandler
from src.handlers.database_handler import DatabaseHandler
from src.handlers.plate_recognizer_handler import PlateRecognizerHandler
from src.logger import logger
from src.schemas.vehicle_detection_request import VehicleDetectionRequest

app = FastAPI()
camera_service = CameraHandler()
plate_service = PlateRecognizerHandler()
db_handler = DatabaseHandler()
country_handler = CountryHandler()

basic_auth = HTTPBasic()

os.makedirs('/app/snapshots', exist_ok=True)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Custom exception handler to log all HTTPExceptions before returning the response"""
    logger.error(f'HTTP Exception: {exc.status_code} - {exc.detail} for url: {request.url}')

    return JSONResponse(
        status_code=exc.status_code,
        content={'detail': exc.detail},
    )


@app.post('/api/vehicle_detected')
async def handle_vehicle_detection(
    request: VehicleDetectionRequest,
    background_tasks: BackgroundTasks,
    credentials: HTTPBasicCredentials = Depends(basic_auth),
):
    if credentials.username != settings.synology_username or credentials.password != settings.synology_password:
        raise HTTPException(status_code=401, detail='Incorrect username or password')

    logger.info(f'Vehicle detected from camera: {request.camera}')

    detection_time = datetime.now()
    timestamp_str = detection_time.strftime('%Y%m%d_%H%M%S')

    background_tasks.add_task(
        process_vehicle_detection,
        request.camera,
        detection_time,
    )

    return {'status': 'accepted', 'timestamp': timestamp_str}


def process_vehicle_detection(camera_name: str, detection_time: datetime):
    """background task for vehicle detection handling

    Args:
        camera_name (str): name of the camera that called the webhook
        detection_time (datetime): time the event was triggered
    """
    try:
        with get_db() as db:
            # Authenticate client
            sid = camera_service.authenticate_client(
                host=settings.synology_host,
                username=settings.synology_username,
                password=settings.synology_password,
            )

            # Get camera data
            cameras = camera_service.get_camera_data(host=settings.synology_host, sid=sid)

            # Find target camera
            target_camera = None
            for camera in cameras:
                if camera.name == camera_name:
                    target_camera = camera
                    break
            if not target_camera:
                raise CameraDataError(f"Camera '{camera_name}' not found in Synology data")

            # Get camera snapshot
            frame = camera_service.get_camera_snapshot(host=settings.synology_host, sid=sid, camera=target_camera)

            image_data = frame.content
            filename = f'observation_{detection_time}.jpg'
            filepath = os.path.join('/app/snapshots', filename)

            # Save image is enabled
            if settings.save_images_for_debug:
                try:
                    with open(filepath, 'wb') as f:
                        f.write(image_data)
                    logger.info(f'Snapshot saved to {filepath}')
                except Exception as e:
                    logger.exception(f'Failed to save image: {e}')

            # Send image to api
            result = plate_service.send_to_api(api_key=settings.api_key, image_data=image_data, camera_name=camera_name)
            if not result:
                logger.info('Plate Recognizer returned no actual observations')
                return
            logger.debug(f'Plate Recognizer results: {result}')

            # Add result to db
            observations_to_create = db_handler.new_observation(
                reader_result=result, detection_timestamp=detection_time
            )

            for observation_data in observations_to_create:
                observation_data = country_handler.get_municipality_and_fix_country(observation=observation_data)
                observation_data = db_handler.hash_plate(observation=observation_data)

                if not db_handler.check_for_duplicates(
                    db=db,
                    observation=observation_data,
                    current_detection_time=detection_time,
                    interval=timedelta(seconds=settings.interval_seconds),
                ):
                    db_handler.create_observation_entry(db=db, observation=observation_data)
    except AuthenticationError as e:
        logger.exception(f'Camera authentication failed: {e}')
        return
    except CameraDataError as e:
        logger.exception(f'Camera data retrieval failed: {e}')
        return
    except SnapshotError as e:
        logger.exception(f'Camera snapshot retrieval failed: {e}')
        return
    except PlateRecognizerCallError as e:
        logger.exception(f'PlateRecognizer API request failed: {e}')
        return
    except DatabaseQueryError as e:
        logger.exception(f'Database query failed: {e}')
        return
    except DatabaseIntegrityError as e:
        logger.exception(f'Database integrity error: {e}')
        return
    except Exception as e:
        logger.exception(f'An unexpected error occurred during background processing: {e}')
        return

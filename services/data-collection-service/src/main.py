import csv
import os
from datetime import datetime

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from src.config import settings
from src.db.session import SessionDep
from src.handlers.camera_handler import CameraHandler
from src.handlers.database_handler import create_vehicle_observation
from src.handlers.municipality_lookup_handler import MunicipalityHandler
from src.handlers.plate_recognizer_handler import PlateRecognizerHandler
from src.schemas.vehicle_detection_request import VehicleDetectionRequest

app = FastAPI()
camera_service = CameraHandler()
plate_service = PlateRecognizerHandler()
municipality_lookup = MunicipalityHandler()

os.makedirs(settings.save_dir, exist_ok=True)


def log_to_csv(data: dict, timestamp: str):
    file_exists = os.path.exists(settings.csv_file)

    with open(settings.csv_file, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if not file_exists:
            writer.writerow(
                [
                    "timestamp",
                    "plate",
                    "confidence",
                    "region",
                    "type",
                    "state",
                    "municipality",
                ]
            )

        for plate in data.get("results", []):
            plate_str = plate.get("plate", "")
            region_code = plate.get("region", {}).get("code", "")
            state, municipality = "", ""

            if region_code == "at":
                state, municipality = municipality_lookup.get_municipality_info(
                    plate_str=plate_str
                )

            writer.writerow(
                [
                    timestamp,
                    plate_str,
                    plate.get("score", ""),
                    region_code,
                    plate.get("vehicle", {}).get("type", ""),
                    state,
                    municipality,
                ]
            )


@app.post("/api/vehicle_detected")
async def handle_vehicle_detection(request: VehicleDetectionRequest, db: SessionDep):
    print(f"Vehicle detected from camera: {request.camera}")

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
            raise HTTPException(
                status_code=404, detail=f"Camera '{request.camera}' not found."
            )

        camera_id = target_camera.id

        frame = camera_service.get_camera_snapshot(
            host=settings.synology_host, sid=sid, camera_id=camera_id
        )

        if not frame:
            raise Exception("Failed to get snapshot")

    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Camera access error: {e}")
        return JSONResponse(
            status_code=500, content={"error": f"Failed to get snapshot: {str(e)}"}
        )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_data = frame.content

    # Save image for debugging if enabled
    if settings.save_images_for_debug:
        filename = f"vehicle_{timestamp}.jpg"
        filepath = os.path.join(settings.save_dir, filename)

        try:
            with open(filepath, "wb") as f:
                f.write(image_data)
            print(f"Snapshot saved to {filepath}")
        except Exception as e:
            print(f"Failed to save image: {e}")

    # Process image with plate recognition
    result = plate_service.send_to_api(image_data=image_data)
    print(result)

    log_to_csv(data=result, timestamp=timestamp)
    from src.enums.vehicle_orientation import VehicleOrientation
    from src.handlers.database_handler import hash_plate
    from src.schemas.vehicle_observation import VehicleObservationCreate

    data = VehicleObservationCreate(
        plate_hash=hash_plate("so986dx"),
        country="AT",
        vehicle_type="car",
        orientation=VehicleOrientation.FRONT,
    )

    try:
        create_vehicle_observation(db=db, observation_raw=data)
        return {"status": "ok", "timestamp": timestamp, "result": result}
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Error: {str(e)}",
        )

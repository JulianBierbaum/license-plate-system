import csv
import json
import os
from datetime import datetime
from io import BytesIO

import requests
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from camera_control import authenticate_client, get_camera_data, get_camera_snapshot

app = FastAPI()

load_dotenv()

CSV_FILE = os.getenv("CSV_FILE")
MUNICIPALITIES_JSON_FILE = os.getenv("MUNICIPALITIES_JSON_FILE")
SAVE_DIR = os.getenv("SAVE_DIR")
SYNOLOGY_HOST = os.getenv("SYNOLOGY_HOST")
USERNAME = os.getenv("SYNOLOGY_USERNAME")
PASSWORD = os.getenv("SYNOLOGY_PASSWORD")
API_KEY = os.getenv("API_KEY")

# Correctly parse the boolean environment variable
SAVE_IMAGES_FOR_DEBUG = os.getenv("SAVE_IMAGES_FOR_DEBUG", "False").lower() == "true"

os.makedirs(SAVE_DIR, exist_ok=True)

MUNICIPALITY_LOOKUP = {}
with open(MUNICIPALITIES_JSON_FILE, encoding="utf-8") as f:
    data = json.load(f)
    for state, municipalities in data.items():
        for municipality_dict in municipalities:
            for code, name in municipality_dict.items():
                MUNICIPALITY_LOOKUP[code.upper()] = (state, name)


def get_municipality_info(plate_str: str):
    if not plate_str or not MUNICIPALITY_LOOKUP:
        return "", ""

    # Check for 2-letter region codes first
    code_2 = plate_str[:2].upper()
    if code_2 in MUNICIPALITY_LOOKUP:
        return MUNICIPALITY_LOOKUP[code_2]

    # Then try 1-letter codes
    code_1 = plate_str[:1].upper()
    if code_1 in MUNICIPALITY_LOOKUP:
        return MUNICIPALITY_LOOKUP[code_1]

    return "", ""


def send_to_api(image_data):
    try:
        image_buffer = BytesIO(image_data)

        response = requests.post(
            "https://api.platerecognizer.com/v1/plate-reader/",
            files={"upload": image_buffer},
            headers={"Authorization": f"Token {API_KEY}"},
        )
        response.raise_for_status()

        return response.json()
    except requests.RequestException as e:
        print(f"API request failed: {e}")
        return None


def log_to_csv(data, timestamp):
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
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

    with open(CSV_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        for plate in data.get("results", []):
            plate_str = plate.get("plate", "")
            region_code = plate.get("region", {}).get("code", "")
            state, municipality = "", ""
            if region_code == "at":
                state, municipality = get_municipality_info(plate_str)

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
async def handle_vehicle_detection():
    print("Vehicle detected!")

    try:
        sid = authenticate_client(SYNOLOGY_HOST, USERNAME, PASSWORD)
        camera_id = get_camera_data(SYNOLOGY_HOST, sid)[0].id
        frame = get_camera_snapshot(SYNOLOGY_HOST, sid, camera_id)
    except Exception as e:
        print(f"Camera access error: {e}")
        return JSONResponse(
            status_code=500, content={"error": "Failed to get snapshot"}
        )

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_data = frame.content
    filename = f"vehicle_{timestamp}.jpg"
    filepath = os.path.join(SAVE_DIR, filename)

    if SAVE_IMAGES_FOR_DEBUG:  # This will now correctly evaluate to True or False
        try:
            with open(filepath, "wb") as f:
                f.write(image_data)
            print(f"Snapshot saved to {filepath}")
        except Exception as e:
            print(f"Failed to save image: {e}")

    result = send_to_api(image_data)

    if result:
        log_to_csv(result, timestamp)

    print(result)

    return {"status": "ok", "timestamp": timestamp, "result": result}

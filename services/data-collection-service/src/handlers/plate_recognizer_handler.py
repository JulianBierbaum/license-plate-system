from io import BytesIO
from typing import Any

import requests

from config import settings


class PlateRecognizerHandler:
    def send_to_api(self, image_data: bytes) -> Any | None:
        try:
            image_buffer = BytesIO(image_data)

            response = requests.post(
                "https://api.platerecognizer.com/v1/plate-reader/",
                files={"upload": image_buffer},
                headers={"Authorization": f"Token {settings.api_key}"},
            )
            response.raise_for_status()

            return response.json()
        except requests.RequestException as e:
            print(f"API request failed: {e}")
            return None

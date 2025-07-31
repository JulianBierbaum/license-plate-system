from io import BytesIO
from typing import Any

import requests

from src.config import settings
from src.logger import logger


class PlateRecognizerHandler:
    """Handler for plate recongition with the PlateRecognizer Snapshot API
    """
    def send_to_api(self, image_data: bytes) -> Any | None:
        """sends a new request to the api

        Args:
            image_data (bytes): snapshot image data

        Returns:
            Any | None: returns the recognition data in json or none
        """
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
            logger.exception(f"API request failed: {e}")
            return None

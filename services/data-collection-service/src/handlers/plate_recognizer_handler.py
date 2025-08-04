from io import BytesIO
from typing import Any

import requests
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_fixed,
)

from src.config import settings
from src.logger import logger


class PlateRecognizerHandler:
    """Handler for plate recongition with the PlateRecognizer Snapshot API"""

    @retry(
        wait=wait_fixed(1),
        stop=stop_after_attempt(5),
        retry=retry_if_exception_type(requests.exceptions.HTTPError),
        reraise=True,
    )
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
                timeout=15,
            )
            response.raise_for_status()

            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"PlateRecognizer API request failed: {e}")
            raise
        except Exception as e:
            logger.exception(f"Error in PlateRecognizerHandler: {e}")
            return None

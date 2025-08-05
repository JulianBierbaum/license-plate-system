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
from src.exceptions.plate_recognizer_exceptions import PlateRecognizerCallError


class PlateRecognizerHandler:
    """Handler for plate recongition with the PlateRecognizer Snapshot API"""

    @retry(
        wait=wait_fixed(1),
        stop=stop_after_attempt(5),
        retry=retry_if_exception_type(requests.HTTPError),
        reraise=True,
    )
    def send_to_api(self, image_data: bytes) -> Any:
        """sends a new request to the api

        Args:
            image_data (bytes): snapshot image data

        Raises:
            PlateRecognizerCallError: raised if the api returns fails
            Exception: thrown on unexpected errors

        Returns:
            Any: response json with plate and vehicle data
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
        except requests.RequestException as e:
            raise PlateRecognizerCallError(
                f"Error when calling the Plate Recognizer api: {e}"
            )
        except Exception:
            raise

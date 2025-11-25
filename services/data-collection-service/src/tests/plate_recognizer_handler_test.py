import pytest
import requests
from unittest.mock import patch, MagicMock

from src.handlers.plate_recognizer_handler import PlateRecognizerHandler
from src.exceptions.plate_recognizer_exceptions import PlateRecognizerCallError


@pytest.fixture
def plate_recognizer_handler():
    """Fixture for PlateRecognizerHandler instance."""
    return PlateRecognizerHandler()


class TestPlateRecognizerHandler:
    def test_send_to_api_success(self, plate_recognizer_handler):
        with patch('requests.post') as mock_post:
            mock_response = MagicMock()
            mock_response.json.return_value = {'results': [{'plate': 'ABC-123'}]}
            mock_response.raise_for_status.return_value = None
            mock_post.return_value = mock_response

            response = plate_recognizer_handler.send_to_api('api_key', b'image_data', 'camera_name', 'service_url')
            assert response == {'results': [{'plate': 'ABC-123'}]}

    def test_send_to_api_failure(self, plate_recognizer_handler):
        with patch('requests.post') as mock_post:
            mock_post.side_effect = requests.exceptions.RequestException
            with pytest.raises(PlateRecognizerCallError):
                plate_recognizer_handler.send_to_api('api_key', b'image_data', 'camera_name', 'service_url')

import pytest
import requests
from unittest.mock import MagicMock, patch

from src.handlers.camera_handler import CameraHandler
from src.exceptions.camera_exceptions import (
    AuthenticationError,
    CameraDataError,
    SnapshotError,
)
from src.schemas.synology_camera import SynologyCamera


@pytest.fixture
def camera_handler():
    """Fixture for CameraHandler instance."""
    return CameraHandler()


class TestCameraHandler:
    def test_authenticate_client_success(self, camera_handler):
        with patch.object(camera_handler.session, 'get') as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = {'data': {'sid': 'test_sid'}}
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response

            sid = camera_handler.authenticate_client('host', 'user', 'pass')
            assert sid == 'test_sid'

    def test_authenticate_client_failure(self, camera_handler):
        with patch.object(camera_handler.session, 'get') as mock_get:
            mock_get.side_effect = requests.exceptions.RequestException
            with pytest.raises(AuthenticationError):
                camera_handler.authenticate_client('host', 'user', 'pass')

    def test_authenticate_client_no_sid(self, camera_handler):
        with patch.object(camera_handler.session, 'get') as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = {'data': {}}  # No sid
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response

            with pytest.raises(AuthenticationError, match='Authentication failed: No SID returned'):
                camera_handler.authenticate_client('host', 'user', 'pass')

    def test_authenticate_client_http_error(self, camera_handler):
        with patch.object(camera_handler.session, 'get') as mock_get:
            mock_response = MagicMock()
            mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError
            mock_get.return_value = mock_response

            with pytest.raises(AuthenticationError, match='Network error during authentication'):
                camera_handler.authenticate_client('host', 'user', 'pass')

    def test_get_camera_data_success(self, camera_handler):
        with patch.object(camera_handler.session, 'get') as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = {
                'data': {
                    'cameras': [
                        {
                            'id': 1,
                            'name': 'Camera 1',
                            'model': 'Model 1',
                            'vendor': 'Vendor 1',
                            'ip': '1.1.1.1',
                            'status': 1,
                        }
                    ]
                }
            }
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response

            cameras = camera_handler.get_camera_data('host', 'sid')
            assert len(cameras) == 1
            assert cameras[0].name == 'Camera 1'

    def test_get_camera_data_failure(self, camera_handler):
        with patch.object(camera_handler.session, 'get') as mock_get:
            mock_get.side_effect = requests.exceptions.RequestException
            with pytest.raises(CameraDataError):
                camera_handler.get_camera_data('host', 'sid')

    def test_get_camera_data_malformed_response(self, camera_handler):
        with patch.object(camera_handler.session, 'get') as mock_get:
            mock_response = MagicMock()
            mock_response.json.return_value = {'data': {'cameras': {'not': 'a list'}}}
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response

            with pytest.raises(CameraDataError, match='Unexpected cameras data format'):
                camera_handler.get_camera_data('host', 'sid')

    def test_get_camera_data_with_malformed_camera(self, camera_handler):
        with (
            patch.object(camera_handler.session, 'get') as mock_get,
            patch('src.handlers.camera_handler.logger.warning') as mock_logger,
        ):
            mock_response = MagicMock()
            mock_response.json.return_value = {
                'data': {
                    'cameras': [
                        {
                            'id': 1,
                            'name': 'Camera 1',
                            'model': 'Model 1',
                            'vendor': 'Vendor 1',
                            'ip': '1.1.1.1',
                            'status': 1,
                        },
                        {
                            'id': 2,
                            'name': 'Malformed Camera',
                            # Missing required fields
                        },
                    ]
                }
            }
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response

            cameras = camera_handler.get_camera_data('host', 'sid')
            assert len(cameras) == 1
            assert cameras[0].name == 'Camera 1'
            mock_logger.assert_called_once()

    def test_get_camera_data_http_error(self, camera_handler):
        with patch.object(camera_handler.session, 'get') as mock_get:
            mock_response = MagicMock()
            mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError
            mock_get.return_value = mock_response

            with pytest.raises(CameraDataError, match='Network error while fetching camera data'):
                camera_handler.get_camera_data('host', 'sid')

    def test_get_camera_by_name_success(self, camera_handler):
        cameras = [
            SynologyCamera(id=1, name='Camera 1', model='Model 1', vendor='Vendor 1', ip='1.1.1.1', status=1),
            SynologyCamera(id=2, name='Camera 2', model='Model 2', vendor='Vendor 2', ip='2.2.2.2', status=1),
        ]
        camera = camera_handler.get_camera_by_name(cameras, 'Camera 1')
        assert camera.name == 'Camera 1'

    def test_get_camera_by_name_failure(self, camera_handler):
        cameras = [
            SynologyCamera(id=1, name='Camera 1', model='Model 1', vendor='Vendor 1', ip='1.1.1.1', status=1),
        ]
        with pytest.raises(CameraDataError):
            camera_handler.get_camera_by_name(cameras, 'Camera 2')

    def test_get_camera_snapshot_success(self, camera_handler):
        with patch.object(camera_handler.session, 'get') as mock_get:
            mock_response = MagicMock()
            mock_response.raise_for_status.return_value = None
            mock_get.return_value = mock_response
            camera = SynologyCamera(id=1, name='Camera 1', model='Model 1', vendor='Vendor 1', ip='1.1.1.1', status=1)

            response = camera_handler.get_camera_snapshot('host', 'sid', camera)

            assert response is not None
            mock_get.assert_called_once()
            call_args = mock_get.call_args
            assert call_args.args[0] == 'host/webapi/entry.cgi'
            expected_params = {
                'api': 'SYNO.SurveillanceStation.Camera',
                'version': '9',
                'id': camera.id,
                'profileType': 0,
                'method': 'GetSnapshot',
                '_sid': 'sid',
            }
            assert call_args.kwargs['params'] == expected_params

    def test_get_camera_snapshot_failure(self, camera_handler):
        with patch.object(camera_handler.session, 'get') as mock_get:
            mock_get.side_effect = requests.exceptions.RequestException
            camera = SynologyCamera(id=1, name='Camera 1', model='Model 1', vendor='Vendor 1', ip='1.1.1.1', status=1)
            with pytest.raises(SnapshotError):
                camera_handler.get_camera_snapshot('host', 'sid', camera)

    def test_get_camera_snapshot_http_error(self, camera_handler):
        with patch.object(camera_handler.session, 'get') as mock_get:
            mock_response = MagicMock()
            mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError
            mock_get.return_value = mock_response
            camera = SynologyCamera(id=1, name='Camera 1', model='Model 1', vendor='Vendor 1', ip='1.1.1.1', status=1)
            with pytest.raises(SnapshotError, match='Network error while fetching snapshot'):
                camera_handler.get_camera_snapshot('host', 'sid', camera)

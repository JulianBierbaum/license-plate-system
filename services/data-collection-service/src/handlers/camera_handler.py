import requests
from requests.exceptions import RequestException

from src.exceptions.camera_exceptions import (
    AuthenticationError,
    CameraDataError,
    SnapshotError,
)
from src.logger import logger
from src.schemas.synology_camera import SynologyCamera


class CameraHandler:
    """Handler function for camera functionality"""

    def __init__(self):
        self.session = requests.Session()

    def authenticate_client(self, host: str, username: str, password: str) -> str:
        """Tries to authenticate client on Surveillance Station.
        Args:
            host (str): ip of the nas
            username (str): Surveillance Station username
            password (str): Surveillance Station password

        Raises:
            AuthenticationError: If authentication fails for any reason.

        Returns:
            str: The session id for the connection.
        """
        try:
            auth_url = f"{host}/webapi/auth.cgi"
            auth_payload = {
                "api": "SYNO.API.Auth",
                "method": "Login",
                "version": "6",
                "account": username,
                "passwd": password,
                "session": "SurveillanceStation",
                "format": "sid",
            }

            res = self.session.get(auth_url, params=auth_payload, verify=False)
            res.raise_for_status()
            json_data = res.json()

            sid = json_data.get("data", {}).get("sid")
            if not sid:
                raise AuthenticationError(
                    f"Authentication failed: No SID returned. Response: {json_data}"
                )

            return sid
        except RequestException as e:
            raise AuthenticationError(
                f"Network error during authentication"
            ) from e
        except Exception:
            raise

    def get_camera_data(self, host: str, sid: str) -> list[SynologyCamera]:
        """Gets data for all cameras connected in the Surveillance Station network.
        Args:
            host (str): ip of the nas
            sid (str): session id for the connection

        Raises:
            CameraDataError: If camera data cannot be fetched or is malformed.

        Returns:
            list[SynologyCamera]: List of camera data.
        """
        try:
            _cameras_list: list[SynologyCamera] = []
            camera_list_url = f"{host}/webapi/entry.cgi"
            camera_list_payload = {
                "api": "SYNO.SurveillanceStation.Camera",
                "version": "9",
                "method": "List",
                "_sid": sid,
            }

            cameras_response = self.session.get(
                camera_list_url, params=camera_list_payload, verify=False
            )
            cameras_response.raise_for_status()

            json_resp = cameras_response.json()
            cameras_data: list[dict] = json_resp.get("data", {}).get("cameras", [])

            if not isinstance(cameras_data, list):
                raise CameraDataError("Unexpected cameras data format. Expected a list")

            for camera_dict in cameras_data:
                try:
                    _cameras_list.append(SynologyCamera(**camera_dict))
                except Exception as e:
                    logger.warning(
                        f"Skipping malformed camera data: {e} - Data: {camera_dict}"
                    )
            return _cameras_list
        except RequestException as e:
            raise CameraDataError(
                f"Network error while fetching camera data."
            ) from e
        except Exception:
            raise

    def get_camera_snapshot(
        self, host: str, sid: str, camera: SynologyCamera
    ) -> requests.Response:
        """Requests snapshot from a selected camera.
        Args:
            host (str): ip of the nas
            sid (str): session if
            camera (SynologyCamera): camera object containing the camera id

        Raises:
            SnapshotError: If the snapshot cannot be retrieved.

        Returns:
            requests.Response: The image data of the snapshot.
        """
        try:
            snapshot_url = f"{host}/webapi/entry.cgi"
            snapshot_payload = {
                "api": "SYNO.SurveillanceStation.Camera",
                "version": "9",
                "id": camera.id,
                "profileType": 0,
                "method": "GetSnapshot",
                "_sid": sid,
            }

            frame = self.session.get(
                snapshot_url, params=snapshot_payload, stream=True, verify=False
            )
            frame.raise_for_status()
            return frame
        except RequestException as e:
            raise SnapshotError(f"Network error while fetching snapshot") from e
        except Exception:
            raise

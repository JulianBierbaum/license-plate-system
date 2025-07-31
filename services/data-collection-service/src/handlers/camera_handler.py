import requests

from src.logger import logger
from src.schemas.synology_camera import SynologyCamera


class CameraHandler:
    """Handler function for camera functionality
    """
    def __init__(self):
        self.session = requests.Session()

    def authenticate_client(self, host: str, username: str, password: str) -> str:
        """tries to authenticate client on Surveillance Station

        Args:
            host (str): ip of the nas
            username (str): Surveillance Station username
            password (str): Surveillance Station password

        Raises:
            Exception: thrown when authentication fails

        Returns:
            str: the session id for the connection
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

            sid = json_data.get("data", {}).get("sid", "")
            if not sid:
                raise Exception(f"Authentication failed: {json_data}")

            return sid
        except requests.RequestException as e:
            logger.exception(f"Network error during authentication: {e}")
        except Exception as e:
            logger.exception(f"Unexpected error during authentication: {e}")

        return ""

    def get_camera_data(self, host: str, sid: str) -> list[SynologyCamera]:
        """Gets data for all cameras connected in the Surveillance Station network

        Args:
            host (str): ip of the nas
            sid (str): session id for the connection

        Returns:
            list[SynologyCamera]: list of camera data including camera ids
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
                logger.error(
                    f"Unexpected cameras data format: {json_resp}. Expected a list of cameras."
                )
                return []

            for camera_dict in cameras_data:
                try:
                    _cameras_list.append(SynologyCamera(**camera_dict))
                except Exception as e:
                    logger.warning(
                        f"Error processing camera data: {e} - Data: {camera_dict}"
                    )

            return _cameras_list

        except requests.RequestException as e:
            logger.exception(f"Network error while fetching camera data: {e}")
        except Exception as e:
            logger.exception(f"Error while fetching camera list from API: {e}")

        return []

    def get_camera_snapshot(
        self, host: str, sid: str, camera: SynologyCamera
    ) -> requests.Response | None:
        """request snapshot from a selected camera

        Args:
            host (str): ip of the nas
            sid (str): session if
            camera (SynologyCamera): camera object containing the camera id

        Returns:
            requests.Response | None: resturns the image data of the snapshot or none if an error is thrown
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

        except requests.RequestException as e:
            logger.exception(f"Network error while fetching snapshot: {e}")
        except Exception as e:
            logger.exception(f"Unexpected error while fetching snapshot {e}")

        return None

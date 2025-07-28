import requests


class SynologyCamera:
    def __init__(self, camera_data):
        self.id = camera_data.get("id")
        self.name = camera_data.get("newName")
        self.enabled = camera_data.get("enabled", False)
        self.model = camera_data.get("model", "Unknown")
        self.vendor = camera_data.get("vendor", "Unknown")
        self.status = camera_data.get("status", "Unknown")
        self.resolution = camera_data.get("resolution", "Unknown")
        self.ip = camera_data.get("host", "Unknown")


class CameraHandler:
    def __init__(self):
        self.session = requests.Session()

    def authenticate_client(self, host: str, username: str, password: str) -> str:
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
                raise ValueError(f"Authentication failed: {json_data}")

            return sid
        except requests.RequestException as e:
            print(f"Network error during authentication: {e}")
        except Exception as e:
            print(f"Unexpected error during authentication: {e}")

        return ""

    def get_camera_data(self, host: str, sid: str) -> list[SynologyCamera]:
        try:
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

            cameras_data = json_resp.get("data", {}).get("cameras", [])
            if not isinstance(cameras_data, list):
                raise ValueError(f"Unexpected cameras data format: {json_resp}")

            result = [SynologyCamera(cam) for cam in cameras_data]
            return result

        except requests.RequestException as e:
            print(f"Network error while fetching camera data: {e}")
        except Exception as e:
            print(f"Unexpected error while fetching camera data: {e}")

        return []

    def get_camera_snapshot(
        self, host: str, sid: str, camera_id: str
    ) -> requests.Response | None:
        try:
            snapshot_url = f"{host}/webapi/entry.cgi"
            snapshot_payload = {
                "api": "SYNO.SurveillanceStation.Camera",
                "version": "9",
                "id": camera_id,
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
            print(f"Network error while fetching snapshot: {e}")
        except Exception as e:
            print(f"Unexpected error while fetching snapshot: {e}")

        return None

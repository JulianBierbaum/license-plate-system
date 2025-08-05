class AuthenticationError(Exception):
    """Raised when authentication with Surveillance Station fails"""

    pass


class CameraDataError(Exception):
    """Raised when camera data cannot be fetched or is malformed"""

    pass


class SnapshotError(Exception):
    """Raised when a camera snapshot cannot be retrieved"""

    pass

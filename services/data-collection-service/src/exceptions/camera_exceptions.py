class CameraException(Exception):
    """Base exception for camera errors"""

    pass


class AuthenticationError(CameraException):
    """Raised when authentication with Surveillance Station fails"""

    pass


class CameraDataError(CameraException):
    """Raised when camera data cannot be fetched or is malformed"""

    pass


class SnapshotError(CameraException):
    """Raised when a camera snapshot cannot be retrieved"""

    pass

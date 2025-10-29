class PlateRecognizerException(Exception):
    """Base exception for Plate Recognizer errors"""

    pass


class PlateRecognizerCallError(PlateRecognizerException):
    """Raised when the api call to Plate Recognizer fails"""

    pass

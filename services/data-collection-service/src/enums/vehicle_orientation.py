from enum import Enum


class VehicleOrientation(str, Enum):
    """Enum for the Orientation of Vehicles

    Args:
        str (orientation): the orientation value
        Enum (name): the orientation key
    """
    FRONT = "front"
    REAR = "rear"

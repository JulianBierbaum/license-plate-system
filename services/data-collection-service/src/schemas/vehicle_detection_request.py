from pydantic import BaseModel, Field


class VehicleDetectionRequest(BaseModel):
    """schema for camera name data when calling the webhook"""

    camera: str = Field(..., max_length=50)

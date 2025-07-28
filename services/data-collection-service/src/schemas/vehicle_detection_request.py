from pydantic import BaseModel


class VehicleDetectionRequest(BaseModel):
    camera: str

from datetime import datetime

from pydantic import BaseModel

from ..enums.vehicle_orientation import VehicleOrientation


# Schema for creating a new observation (e.g., in a POST request)
class VehicleObservationCreate(BaseModel):
    plate_hash: bytes
    country: str | None = None
    vehicle_type: str | None = None
    orientation: VehicleOrientation | None = None


# Schema for responding with observation data (e.g., in a GET request)
class VehicleObservationResponse(BaseModel):
    id: int
    timestamp: datetime
    plate_hash: bytes
    country: str | None = None
    vehicle_type: str | None = None
    orientation: VehicleOrientation | None = None

    class Config:
        from_attributes = True

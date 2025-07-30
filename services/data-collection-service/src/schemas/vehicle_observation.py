from datetime import datetime

from pydantic import BaseModel, Field

from src.enums.vehicle_orientation import VehicleOrientation


class VehicleObservationBase(BaseModel):
    country_code: str | None = Field(None, max_length=10)
    vehicle_type: str | None = Field(None, max_length=30)
    orientation: VehicleOrientation | None = None
    timestamp: datetime = Field(default_factory=datetime.now)


class VehicleObservationRaw(VehicleObservationBase):
    plate: str = Field(..., max_length=30)


class VehicleObservationCreate(VehicleObservationBase):
    plate_hash: bytes = Field(..., min_length=32, max_length=32)

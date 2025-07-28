from pydantic import BaseModel

from src.enums.vehicle_orientation import VehicleOrientation


class VehicleObservationCreate(BaseModel):
    plate_hash: bytes
    country: str | None = None
    vehicle_type: str | None = None
    orientation: VehicleOrientation | None = None

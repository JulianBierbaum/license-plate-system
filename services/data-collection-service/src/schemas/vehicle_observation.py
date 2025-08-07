from datetime import datetime

from pydantic import BaseModel, Field

from src.enums.vehicle_orientation import VehicleOrientation


class VehicleObservationBase(BaseModel):
    """vehicle observation base model"""

    plate_score: int | None = None
    country_code: str | None = Field(None, max_length=10)
    municipality: str | None = Field(None, max_length=10)
    vehicle_type: str | None = Field(None, max_length=30)
    make: str | None = Field(None, max_length=30)
    model: str | None = Field(None, max_length=50)
    color: str | None = Field(None, max_length=30)
    orientation: VehicleOrientation | None = None
    timestamp: datetime = Field(default_factory=datetime.now)


class VehicleObservationRaw(VehicleObservationBase):
    """vehicle obervation schema with plain text plate

    Args:
        VehicleObservationBase (pydantic): base schema
    """

    plate: str = Field(..., max_length=30)


class VehicleObservationCreate(VehicleObservationBase):
    """vehicle obervation schema with hashed plate

    Args:
        VehicleObservationBase (pydantic): base schema
    """

    plate_hash: bytes = Field(..., min_length=32, max_length=32)

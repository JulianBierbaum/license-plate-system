from sqlalchemy import Column, DateTime, Integer, LargeBinary, String
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.sql import func

from ..enums.vehicle_orientation import VehicleOrientation

# relative imports needed for db-prestart service
from ..models.base import IngestionBase


class VehicleObservation(IngestionBase):
    """SQLAlchemy model for the vehicle observation objects

    Args:
        IngestionBase (postgres schema): base for the ingestion schema
    """

    __tablename__ = "vehicle_observations"

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    timestamp = Column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
        server_default=func.now(),
    )
    plate_hash = Column(
        LargeBinary(32),
        nullable=False,
        index=True,
    )
    plate_score = Column(
        Integer,
        nullable=True,
    )
    country_code = Column(
        String(10),
        nullable=True,
    )
    municipality = Column(
        String(10),
        nullable=True,
    )
    vehicle_type = Column(
        String(30),
        nullable=True,
    )
    make = Column(
        String(30),
        nullable=True,
    )
    model = Column(
        String(50),
        nullable=True,
    )
    color = Column(
        String(30),
        nullable=True,
    )
    orientation = Column(
        ENUM(VehicleOrientation, name="vehicle_orientation"),
        nullable=True,
    )

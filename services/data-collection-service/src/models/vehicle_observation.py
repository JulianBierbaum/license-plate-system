from sqlalchemy import Column, DateTime, Index, Integer, LargeBinary, String
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.sql import func

from ..enums.vehicle_orientation import VehicleOrientation

# relative imports needed for db-migrator service
from ..models.base import IngestionBase


class VehicleObservation(IngestionBase):
    """SQLAlchemy model for the vehicle observation objects

    Args:
        IngestionBase (postgres schema): base for the ingestion schema
    """
    __tablename__ = "vehicle_observations"
    __table_args__ = (
        Index("idx_vehicle_observations_timestamp", "timestamp"),
        Index("idx_vehicle_observations_plate_hash", "plate_hash"),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    plate_hash = Column(
        LargeBinary(32),
        nullable=False,
    )
    plate_score = Column(
        Integer,
        nullable=True,
    )
    country_code = Column(
        String(10),
        nullable=True,
    )
    vehicle_type = Column(
        String(30),
        nullable=True,
    )

    orientation = Column(
        ENUM(VehicleOrientation, name="vehicle_orientation"),
        nullable=True,
    )

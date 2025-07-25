from datetime import datetime, timezone
import enum

from sqlalchemy import (
    Column,
    DateTime,
    Index,
    Integer,
    LargeBinary,
    MetaData,
    String,
    func,
)
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.declarative import declarative_base


class VehicleOrientation(enum.Enum):
    FRONT = "front"
    REAR = "rear"

# Create metadata with schema specification
metadata_data_collection = MetaData(schema="ingestion_schema")
Base = declarative_base(metadata=metadata_data_collection)


class VehicleObservation(Base):
    __tablename__ = "vehicle_observations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )

    plate_hash = Column(LargeBinary(32), nullable=False) # SHA256 hash
    country = Column(String(5), nullable=True)
    vehicle_type = Column(String(50), nullable=True)

    orientation = Column(
        postgresql.ENUM(
            VehicleOrientation,
            name='vehicle_orientation',
            create_type=True,
            nullable=True
        ),
        nullable=True
    )

    __table_args__ = (
        Index("idx_vehicle_observations_timestamp", "timestamp"),
        Index("idx_vehicle_observations_plate_hash", "plate_hash"),
    )

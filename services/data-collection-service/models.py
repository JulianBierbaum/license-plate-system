from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    Index,
    Integer,
    MetaData,
    String,
)
from sqlalchemy.ext.declarative import declarative_base

# Create metadata with schema specification
metadata_data_collection = MetaData(schema="ingestion_schema")
Base = declarative_base(metadata=metadata_data_collection)


class VehicleObservation(Base):
    __tablename__ = "vehicle_observations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    plate = Column(String(10), nullable=False)
    confidence = Column(Float, nullable=False)
    region = Column(String(5), nullable=True)
    vehicle_type = Column(String(50), nullable=True)
    state = Column(String(100), nullable=True)
    municipality = Column(String(100), nullable=True)
    status = Column(String, nullable=True)

    __table_args__ = (
        Index("idx_vehicle_observations_timestamp", "timestamp"),
        Index("idx_vehicle_observations_plate", "plate"),
        Index("idx_vehicle_observations_municipality", "municipality"),
    )

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    MetaData,
    Index,
)
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# Create metadata with schema specification
metadata_data_collection = MetaData(schema="ingestion_schema")
Base = declarative_base(metadata=metadata_data_collection)

class VehicleObservation(Base):
    __tablename__ = 'vehicle_observations'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.utcnow)
    plate = Column(String(10), nullable=False)
    confidence = Column(Float, nullable=False)
    region = Column(String(5), nullable=True)
    vehicle_type = Column(String(50), nullable=True)
    state = Column(String(100), nullable=True)
    municipality = Column(String(100), nullable=True)
    
    __table_args__ = (
        Index('idx_vehicle_observations_timestamp', 'timestamp'),
        Index('idx_vehicle_observations_plate', 'plate'),
        Index('idx_vehicle_observations_municipality', 'municipality'),
    )

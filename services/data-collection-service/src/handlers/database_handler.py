from hashlib import sha256

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.models.vehicle_observation import VehicleObservation
from src.schemas.vehicle_observation import VehicleObservationCreate


def hash_plate(plate: str) -> bytes:
    normalized = plate.strip().lower()
    return sha256(normalized.encode("utf-8")).digest()


def create_vehicle_observation(
    db: Session, observation_raw: VehicleObservationCreate
) -> VehicleObservation:
    db_observation = VehicleObservation(
        plate_hash=observation_raw.plate_hash,
        country=observation_raw.country,
        vehicle_type=observation_raw.vehicle_type,
        orientation=observation_raw.orientation,
    )

    try:
        db.add(db_observation)
        db.commit()
        db.refresh(db_observation)
        return db_observation
    except IntegrityError as e:
        db.rollback()
        raise e

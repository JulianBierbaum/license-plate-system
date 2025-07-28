from hashlib import sha256

from sqlalchemy.orm import Session

from ..models.vehicle_obervation import VehicleObservation
from ..enums.vehicle_orientation import VehicleOrientation


def hash_plate(plate: str) -> bytes:
    normalized = plate.strip().lower()
    return sha256(normalized.encode("utf-8")).digest()


def create_vehicle_observation(session: Session) -> VehicleObservation:
    observation = VehicleObservation(
        plate_hash=hash_plate("so986dx"),
        country="AT",
        vehicle_type="car",
        orientation=VehicleOrientation.FRONT,
    )
    session.add(observation)
    session.commit()
    session.refresh(observation)

    return observation

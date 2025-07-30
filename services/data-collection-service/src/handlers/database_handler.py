from datetime import datetime, timedelta
from hashlib import sha256
from typing import Any

from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.enums.vehicle_orientation import VehicleOrientation
from src.logger import logger
from src.models.vehicle_observation import VehicleObservation
from src.schemas.vehicle_observation import (
    VehicleObservationCreate,
    VehicleObservationRaw,
)


class DatabaseHandler:
    def new_observation(
        self, reader_result: Any, detection_timestamp: datetime
    ) -> list[VehicleObservationRaw]:
        _observation_list: list = []

        results_list = reader_result.get("results", [])

        if not results_list:
            logger.info("No vehicle observations found in reader result.")
            return _observation_list

        for observation in results_list:
            data = VehicleObservationRaw(
                plate=observation.get("plate", ""),
                country_code=observation.get("region", {}).get("code", ""),
                vehicle_type=observation.get("vehicle", {}).get("type", ""),
                orientation=VehicleOrientation.FRONT,  # PLACEHOLDER UNTIL LICENSE UPGRADE
                timestamp=detection_timestamp,
            )
            _observation_list.append(data)
        return _observation_list

    def check_for_duplicates(
        self,
        db: Session,
        observation: VehicleObservationCreate,
        current_detection_time: datetime,
    ) -> bool:
        one_minute_before_detection = current_detection_time - timedelta(minutes=1)
        duplicate_observation = (
            db.query(VehicleObservation)
            .filter(
                and_(
                    VehicleObservation.plate_hash == observation.plate_hash,
                    VehicleObservation.timestamp >= one_minute_before_detection,
                    VehicleObservation.timestamp
                    <= current_detection_time,  # If the entry is in the future for sume reason
                )
            )
            .first()
        )
        return duplicate_observation is not None  # True on Duplicate found

    def hash_plate(
        self, observation: VehicleObservationRaw
    ) -> VehicleObservationCreate:
        normalized = observation.plate.strip().lower()
        logger.debug(f"Plate: {normalized}")

        return VehicleObservationCreate(
            plate_hash=sha256(normalized.encode("utf-8")).digest(),
            country_code=observation.country_code,
            vehicle_type=observation.vehicle_type,
            orientation=observation.orientation,
            timestamp=observation.timestamp,
        )

    def create_observation_entry(
        self, db: Session, observation: VehicleObservationCreate
    ) -> VehicleObservation | None:
        db_observation = VehicleObservation(
            plate_hash=observation.plate_hash,
            country_code=observation.country_code,
            vehicle_type=observation.vehicle_type,
            orientation=observation.orientation,
            timestamp=observation.timestamp,
        )

        try:
            db.add(db_observation)
            db.commit()
            db.refresh(db_observation)

            logger.info(
                f"Observation saved. ID: {db_observation.id}, "
                f"Timestamp: {db_observation.timestamp}, "
                f"Plate Hash: {db_observation.plate_hash.hex()}, "
                f"Region: {db_observation.country_code}, "
                f"Vehicle Type: {db_observation.vehicle_type}, "
                f"Orientation: {db_observation.orientation.value}"
            )
            return db_observation
        except IntegrityError as e:
            logger.exception(f"Error creating observation entry: {e}")

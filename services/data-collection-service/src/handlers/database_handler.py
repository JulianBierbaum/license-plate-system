from datetime import datetime, timedelta
from hashlib import sha256
from typing import Any

from sqlalchemy import and_, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.enums.vehicle_orientation import VehicleOrientation
from src.exceptions.database_exceptions import (
    DatabaseIntegrityError,
    DatabaseQueryError,
)
from src.logger import logger
from src.models.vehicle_observation import VehicleObservation
from src.schemas.vehicle_observation import (
    VehicleObservationCreate,
    VehicleObservationRaw,
)


class DatabaseHandler:
    """Handler for the connections to the database and saving new vehicle observations"""

    def new_observation(
        self, reader_result: Any, detection_timestamp: datetime
    ) -> list[VehicleObservationRaw]:
        """extracts obervation data from analyzer result json

        Args:
            reader_result (Any): analyzer results in json format
            detection_timestamp (datetime): timestamp when the webhook was called

        Returns:
            list[VehicleObservationRaw]: list of vehicle obervation objects
        """
        _observation_list: list = []
        results_list = reader_result.get("results", [])

        if not results_list:
            logger.info("No vehicle observations found in reader result.")
            return _observation_list

        for observation in results_list:
            try:
                data = VehicleObservationRaw(
                    plate=observation.get("plate", ""),
                    plate_score=int(observation["candidates"][0]["score"] * 1000),
                    country_code=observation.get("region", {}).get("code", ""),
                    vehicle_type=observation.get("vehicle", {}).get("type", ""),
                    orientation=VehicleOrientation.FRONT,
                    timestamp=detection_timestamp,
                )
                _observation_list.append(data)
            except (KeyError, IndexError, TypeError) as e:
                logger.exception(
                    f"Malformed observation entry: {e}. Data: {observation}"
                )
                continue
        return _observation_list

    def check_for_duplicates(
        self,
        db: Session,
        observation: VehicleObservationCreate,
        current_detection_time: datetime,
    ) -> bool:
        """checks if an observation with the same plate was saved in the last minute

        Args:
            db (Session): db session
            observation (VehicleObservationCreate): vehicle observation object
            current_detection_time (datetime): time of the detection
        Raises:
            DatabaseQueryError: raised when an error occures in the db query

        Returns:
            bool: returns true if a duplicate is found
        """
        try:
            one_minute_before_detection = current_detection_time - timedelta(minutes=1)
            stmt = select(
                VehicleObservation
            ).where(
                and_(
                    VehicleObservation.plate_hash == observation.plate_hash,
                    VehicleObservation.timestamp >= one_minute_before_detection,
                    VehicleObservation.timestamp
                    <= current_detection_time,  # If the entry is in the future for sume reason
                )
            )
            duplicate_observation = db.execute(stmt).scalars().first()
            return duplicate_observation is not None
        except SQLAlchemyError as e:
            raise DatabaseQueryError("Error while checking for duplicates") from e

    def hash_plate(
        self, observation: VehicleObservationRaw
    ) -> VehicleObservationCreate:
        """method for hashing plates for anonymisation in storage

        Args:
            observation (VehicleObservationRaw): vehicle observation object with plain plate

        Returns:
            VehicleObservationCreate: vehicle observation object with hashed plate
        """
        normalized = observation.plate.strip().lower()
        logger.debug(f"Plate: {normalized}")

        return VehicleObservationCreate(
            plate_hash=sha256(normalized.encode("utf-8")).digest(),
            plate_score=observation.plate_score,
            country_code=observation.country_code,
            vehicle_type=observation.vehicle_type,
            orientation=observation.orientation,
            timestamp=observation.timestamp,
        )

    def create_observation_entry(
        self, db: Session, observation: VehicleObservationCreate
    ) -> VehicleObservation | None:
        """creates a new entry in the db

        Args:
            db (Session): db session
            observation (VehicleObservationCreate): observation object for db insertion

        Raises:
            DatabaseIntegrityError: raised when the database throws an integrity error

        Returns:
            VehicleObservation | None: returns object or none on failure
        """
        db_observation = VehicleObservation(
            plate_hash=observation.plate_hash,
            plate_score=observation.plate_score,
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
        except SQLAlchemyError as e:
            raise DatabaseIntegrityError("Insertion into database failed") from e

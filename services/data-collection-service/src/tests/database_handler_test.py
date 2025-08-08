from datetime import datetime, timedelta, timezone
from hashlib import sha256

import pytest

from src.enums.vehicle_orientation import VehicleOrientation
from src.handlers.database_handler import DatabaseHandler
from src.models.vehicle_observation import VehicleObservation
from src.schemas.vehicle_observation import (
    VehicleObservationCreate,
    VehicleObservationRaw,
)


@pytest.fixture
def db_handler():
    """Fixture for DatabaseHandler instance."""
    return DatabaseHandler()


# --- Tests for new_observation ---
def test_new_observation_successful_extraction(db_handler):
    """
    Test successful extraction of a single observation from reader_result.
    """
    detection_timestamp = datetime(2025, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
    reader_result = {
        'results': [
            {
                'plate': 'ABC1234',
                'candidates': [{'score': 0.95}],
                'region': {'code': 'US'},
                'vehicle': {'type': 'car'},
                'model_make': [{'make': 'Toyota', 'model': 'Corolla', 'score': 0.9}],
                'color': [{'color': 'red', 'score': 0.8}],
                'orientation': [{'orientation': 'Front', 'score': 1.0}],
            }
        ]
    }

    observations = db_handler.new_observation(reader_result, detection_timestamp)

    assert len(observations) == 1
    obs = observations[0]
    assert obs.plate == 'ABC1234'
    assert obs.plate_score == 950
    assert obs.country_code == 'US'
    assert obs.vehicle_type == 'car'
    assert obs.make == 'Toyota'
    assert obs.model == 'Corolla'
    assert obs.color == 'red'
    assert obs.orientation == VehicleOrientation.FRONT
    assert obs.timestamp == detection_timestamp


def test_new_observation_empty_results(db_handler):
    """
    Test when reader_result has an empty 'results' list.
    """
    detection_timestamp = datetime(2025, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
    reader_result = {'results': []}

    observations = db_handler.new_observation(reader_result, detection_timestamp)
    assert len(observations) == 0


def test_new_observation_multiple_observations(db_handler):
    """
    Test extraction of multiple observations from reader_result.
    """
    detection_timestamp = datetime(2025, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
    reader_result = {
        'results': [
            {
                'plate': 'ABC1234',
                'candidates': [{'score': 0.95}],
                'region': {'code': 'US'},
                'vehicle': {'type': 'car'},
                'model_make': [{'make': 'Toyota', 'model': 'Corolla', 'score': 0.9}],
                'color': [{'color': 'red', 'score': 0.8}],
                'orientation': [{'orientation': 'Front', 'score': 1.0}],
            },
            {
                'plate': 'XYZ789',
                'candidates': [{'score': 0.88}],
                'region': {'code': 'CA'},
                'vehicle': {'type': 'truck'},
                'model_make': [{'make': 'Ford', 'model': 'F-150', 'score': 0.85}],
                'color': [{'color': 'blue', 'score': 0.7}],
                'orientation': [{'orientation': 'Rear', 'score': 1.0}],
            },
        ]
    }

    observations = db_handler.new_observation(reader_result, detection_timestamp)
    assert len(observations) == 2
    obs1, obs2 = observations
    assert obs1.plate == 'ABC1234'
    assert obs1.make == 'Toyota'
    assert obs1.model == 'Corolla'
    assert obs1.color == 'red'
    assert obs1.orientation == VehicleOrientation.FRONT

    assert obs2.plate == 'XYZ789'
    assert obs2.make == 'Ford'
    assert obs2.model == 'F-150'
    assert obs2.color == 'blue'
    assert obs2.orientation == VehicleOrientation.REAR


# --- Tests for hash_plate ---
def test_hash_plate_standard(db_handler):
    """
    Test hashing a standard plate.
    """
    raw_obs = VehicleObservationRaw(
        plate='TEST123',
        plate_score=900,
        country_code='US',
        vehicle_type='car',
        make='Toyota',
        model='Corolla',
        color='red',
        orientation=VehicleOrientation.FRONT,
        timestamp=datetime.now(),
    )
    hashed_obs = db_handler.hash_plate(raw_obs)
    expected_hash = sha256(b'test123').digest()

    assert hashed_obs.plate_hash == expected_hash
    assert hashed_obs.plate_score == raw_obs.plate_score
    assert hashed_obs.country_code == raw_obs.country_code
    assert hashed_obs.vehicle_type == raw_obs.vehicle_type
    assert hashed_obs.make == raw_obs.make
    assert hashed_obs.model == raw_obs.model
    assert hashed_obs.color == raw_obs.color
    assert hashed_obs.orientation == raw_obs.orientation
    assert hashed_obs.timestamp == raw_obs.timestamp


def test_hash_plate_with_spaces_and_case(db_handler):
    """
    Test hashing a plate with leading/trailing spaces and different casing.
    """
    raw_obs = VehicleObservationRaw(
        plate='  AbC 456  ',
        plate_score=900,
        country_code='US',
        vehicle_type='car',
        make='Toyota',
        model='Corolla',
        color='red',
        orientation=VehicleOrientation.FRONT,
        timestamp=datetime.now(),
    )
    hashed_obs = db_handler.hash_plate(raw_obs)
    expected_hash = sha256(b'abc 456').digest()  # Stripped and lowercased

    assert hashed_obs.plate_hash == expected_hash


def test_hash_plate_empty_string(db_handler):
    """
    Test hashing an empty plate string.
    """
    raw_obs = VehicleObservationRaw(
        plate='',
        plate_score=900,
        country_code='US',
        vehicle_type='car',
        make='Toyota',
        model='Corolla',
        color='red',
        orientation=VehicleOrientation.FRONT,
        timestamp=datetime.now(),
    )
    hashed_obs = db_handler.hash_plate(raw_obs)
    expected_hash = sha256(b'').digest()

    assert hashed_obs.plate_hash == expected_hash


# --- Tests for check_for_duplicates ---
def create_hashed_observation(plate: str, timestamp: datetime) -> VehicleObservationCreate:
    """Helper to create a VehicleObservationCreate object for testing."""
    return VehicleObservationCreate(
        plate_hash=sha256(plate.strip().lower().encode('utf-8')).digest(),
        plate_score=800,
        country_code='DE',
        vehicle_type='bus',
        make='Mercedes',
        model='Citaro',
        color='yellow',
        orientation=VehicleOrientation.REAR,
        timestamp=timestamp,
    )


def test_check_for_duplicates_no_duplicate(db_handler, db):
    """
    Test no duplicate found when no matching observation exists.
    """
    current_time = datetime(2025, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
    obs_to_check = create_hashed_observation('NEWPLATE', current_time)

    # Insert an unrelated observation
    db_handler.create_observation_entry(
        db, create_hashed_observation('OTHERPLATE', current_time - timedelta(minutes=5))
    )

    is_duplicate = db_handler.check_for_duplicates(db, obs_to_check, current_time, timedelta(seconds=60))
    assert not is_duplicate


def test_check_for_duplicates_exact_duplicate_within_window(db_handler, db):
    """
    Test duplicate found when an exact matching observation exists within 1 minute.
    """
    current_time = datetime(2025, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
    plate_to_check = 'DUPLICATE'
    obs_to_check = create_hashed_observation(plate_to_check, current_time)

    # Insert a duplicate observation 30 seconds ago
    existing_obs_time = current_time - timedelta(seconds=30)
    db_handler.create_observation_entry(db, create_hashed_observation(plate_to_check, existing_obs_time))

    is_duplicate = db_handler.check_for_duplicates(db, obs_to_check, current_time, timedelta(seconds=60))
    assert is_duplicate


def test_check_for_duplicates_duplicate_outside_window_older(db_handler, db):
    """
    Test no duplicate found when a matching observation exists but is older than 1 minute.
    """
    current_time = datetime(2025, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
    plate_to_check = 'OLDPLATE'
    obs_to_check = create_hashed_observation(plate_to_check, current_time)

    # Insert an observation 2 minutes ago
    existing_obs_time = current_time - timedelta(minutes=2)
    db_handler.create_observation_entry(db, create_hashed_observation(plate_to_check, existing_obs_time))

    is_duplicate = db_handler.check_for_duplicates(db, obs_to_check, current_time, timedelta(seconds=60))
    assert not is_duplicate


def test_check_for_duplicates_duplicate_outside_window_newer(db_handler, db):
    """
    Test no duplicate found when a matching observation exists but is newer (in the "future"
    relative to current_detection_time), which shouldn't count based on the query.
    """
    current_time = datetime(2025, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
    plate_to_check = 'FUTUREPLATE'
    obs_to_check = create_hashed_observation(plate_to_check, current_time)

    # Insert an observation 30 seconds in the future
    existing_obs_time = current_time + timedelta(seconds=30)
    db_handler.create_observation_entry(db, create_hashed_observation(plate_to_check, existing_obs_time))

    is_duplicate = db_handler.check_for_duplicates(db, obs_to_check, current_time, timedelta(seconds=60))
    assert not is_duplicate


def test_check_for_duplicates_different_plate_same_time(db_handler, db):
    """
    Test no duplicate found when observations have different plate hashes.
    """
    current_time = datetime(2025, 1, 1, 10, 0, 0, tzinfo=timezone.utc)
    obs_to_check = create_hashed_observation('PLATE1', current_time)

    # Insert a different plate at the same time
    db_handler.create_observation_entry(db, create_hashed_observation('PLATE2', current_time))

    is_duplicate = db_handler.check_for_duplicates(db, obs_to_check, current_time, timedelta(seconds=60))
    assert not is_duplicate


# --- Tests for create_observation_entry ---
def test_create_observation_entry_successful(db_handler, db):
    """
    Test successful creation of a new observation entry.
    """
    hashed_obs = VehicleObservationCreate(
        plate_hash=sha256(b'TESTPLATE').digest(),
        plate_score=999,
        country_code='DE',
        vehicle_type='motorcycle',
        make='BMW',
        model='R1250',
        color='black',
        orientation=VehicleOrientation.FRONT,
        timestamp=datetime.now(tz=timezone.utc),
    )

    created_obs = db_handler.create_observation_entry(db, hashed_obs)

    assert created_obs is not None
    assert created_obs.id is not None
    assert created_obs.plate_hash == hashed_obs.plate_hash
    assert created_obs.plate_score == hashed_obs.plate_score
    assert created_obs.country_code == hashed_obs.country_code
    assert created_obs.vehicle_type == hashed_obs.vehicle_type
    assert created_obs.make == hashed_obs.make
    assert created_obs.model == hashed_obs.model
    assert created_obs.color == hashed_obs.color
    assert created_obs.orientation == hashed_obs.orientation
    assert created_obs.timestamp == hashed_obs.timestamp

    # Verify that the observation exists in the database
    retrieved_obs = db.query(VehicleObservation).filter_by(id=created_obs.id).first()
    assert retrieved_obs is not None
    assert retrieved_obs.plate_hash == created_obs.plate_hash

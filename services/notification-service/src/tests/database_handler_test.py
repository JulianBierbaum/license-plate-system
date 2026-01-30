import pytest
from sqlalchemy.orm import Session

from src.handlers import database_handler as db_handler
from src.models.user_preferences import UserPreferences
from src.schemas.user_preferences import UserPreferencesCreate, UserPreferencesUpdate
from src.exceptions.database_exceptions import (
    DuplicateEntryError,
    MissingEntryError,
)


def create_user_preference_entry(
    db: Session, name: str, email: str, receive_alerts: bool = True, receive_updates: bool = False
) -> UserPreferences:
    """Helper to create a UserPreferences entry for testing."""
    user_pref = UserPreferencesCreate(
        name=name,
        email=email,
        receive_alerts=receive_alerts,
        receive_updates=receive_updates,
    )
    return db_handler.create_new_entry(db, user_pref)


def test_create_new_entry_successful(db: Session):
    """
    Test successful creation of a new user preference entry.
    """
    name = 'test_user'
    email = 'test@example.com'
    user_pref_in = UserPreferencesCreate(
        name=name,
        email=email,
        receive_alerts=True,
        receive_updates=False,
    )

    created_pref = db_handler.create_new_entry(db, user_pref_in)

    assert created_pref is not None
    assert created_pref.id is not None
    assert created_pref.name == name
    assert created_pref.email == email
    assert created_pref.receive_alerts is True
    assert created_pref.receive_updates is False

    retrieved_pref = db.query(UserPreferences).filter_by(id=created_pref.id).first()
    assert retrieved_pref is not None
    assert retrieved_pref.name == name


def test_create_new_entry_duplicate_email(db: Session):
    """
    Test that creating an entry with a duplicate email raises DuplicateEntryError.
    """
    email = 'duplicate@example.com'
    create_user_preference_entry(db, 'first_user', email)

    with pytest.raises(DuplicateEntryError):
        create_user_preference_entry(db, 'second_user', email)


def test_get_entry_found(db: Session):
    """
    Test retrieving an existing entry by ID.
    """
    created_pref = create_user_preference_entry(db, 'get_user', 'get@example.com')
    retrieved_pref = db_handler.get_entry(db, created_pref.id)

    assert retrieved_pref is not None
    assert retrieved_pref.id == created_pref.id
    assert retrieved_pref.name == 'get_user'


def test_get_entry_not_found(db: Session):
    """
    Test that retrieving a non-existent entry by ID returns None.
    """
    retrieved_pref = db_handler.get_entry(db, 9999)
    assert retrieved_pref is None


def test_get_entry_by_name_found(db: Session):
    """
    Test retrieving an existing entry by name.
    """
    name = 'find_by_name'
    create_user_preference_entry(db, name, 'find_by_name@example.com')
    retrieved_pref = db_handler.get_entry_by_name(db, name)

    assert retrieved_pref is not None
    assert retrieved_pref.name == name


def test_get_entry_by_name_not_found(db: Session):
    """
    Test that retrieving a non-existent entry by name returns None.
    """
    retrieved_pref = db_handler.get_entry_by_name(db, 'non_existent_user')
    assert retrieved_pref is None


def test_get_entry_by_email_found(db: Session):
    """
    Test retrieving an existing entry by email.
    """
    email = 'find_by_email@example.com'
    create_user_preference_entry(db, 'find_by_email_user', email)
    retrieved_pref = db_handler.get_entry_by_email(db, email)

    assert retrieved_pref is not None
    assert retrieved_pref.email == email


def test_get_entry_by_email_not_found(db: Session):
    """
    Test that retrieving a non-existent entry by email returns None.
    """
    retrieved_pref = db_handler.get_entry_by_email(db, 'non_existent@example.com')
    assert retrieved_pref is None


def test_get_entries_multiple(db: Session):
    """
    Test retrieving all user preference entries.
    """
    create_user_preference_entry(db, 'user1', 'user1@example.com')
    create_user_preference_entry(db, 'user2', 'user2@example.com')

    all_prefs = db_handler.get_entries(db)
    assert len(all_prefs) == 2


def test_get_entries_empty(db: Session):
    """
    Test retrieving entries when the table is empty.
    """
    all_prefs = db_handler.get_entries(db)
    assert len(all_prefs) == 0


def test_update_entry_successful(db: Session):
    """
    Test successfully updating an existing user preference entry.
    """
    created_pref = create_user_preference_entry(db, 'update_user', 'update@example.com')
    update_data = UserPreferencesUpdate(
        name='updated_user_name',
        email='updated_email@example.com',
        receive_alerts=False,
    )

    updated_pref = db_handler.update_entry(db, update_data, created_pref.id)

    assert updated_pref is not None
    assert updated_pref.id == created_pref.id
    assert updated_pref.name == 'updated_user_name'
    assert updated_pref.email == 'updated_email@example.com'
    assert updated_pref.receive_alerts is False
    assert updated_pref.receive_updates is False


def test_update_entry_not_found(db: Session):
    """
    Test that updating a non-existent entry raises MissingEntryError.
    """
    update_data = UserPreferencesUpdate(name='any_name')
    with pytest.raises(MissingEntryError):
        db_handler.update_entry(db, update_data, 9999)


def test_update_entry_duplicate_email(db: Session):
    """
    Test that updating an entry to an email that already exists raises DuplicateEntryError.
    """
    create_user_preference_entry(db, 'user1', 'existing_email@example.com')
    user_to_update = create_user_preference_entry(db, 'user2', 'email_to_update@example.com')

    update_data = UserPreferencesUpdate(email='existing_email@example.com')
    with pytest.raises(DuplicateEntryError):
        db_handler.update_entry(db, update_data, user_to_update.id)


def test_delete_entry_successful(db: Session):
    """
    Test successfully deleting a user preference entry.
    """
    created_pref = create_user_preference_entry(db, 'delete_user', 'delete@example.com')
    result = db_handler.delete_entry(db, created_pref.id)

    assert result is True
    assert db_handler.get_entry(db, created_pref.id) is None


def test_delete_entry_not_found(db: Session):
    """
    Test that deleting a non-existent entry raises MissingEntryError.
    """
    with pytest.raises(MissingEntryError):
        db_handler.delete_entry(db, 9999)


def test_get_entries_by_preference_alerts(db: Session):
    """
    Test filtering entries by receive_alerts preference.
    """
    create_user_preference_entry(db, 'alert_user', 'alert@example.com', receive_alerts=True)
    create_user_preference_entry(db, 'no_alert_user', 'noalert@example.com', receive_alerts=False)

    alert_users = db_handler.get_entries_by_preference(db, receive_alerts=True)
    assert len(alert_users) == 1
    assert alert_users[0].name == 'alert_user'


def test_get_entries_by_preference_updates(db: Session):
    """
    Test filtering entries by receive_updates preference.
    """
    create_user_preference_entry(db, 'update_user', 'update@example.com', receive_updates=True)
    create_user_preference_entry(db, 'no_update_user', 'noupdate@example.com', receive_updates=False)

    update_users = db_handler.get_entries_by_preference(db, receive_updates=True)
    assert len(update_users) == 1
    assert update_users[0].name == 'update_user'


def test_get_entries_by_names(db: Session):
    """
    Test retrieving entries by a list of names.
    """
    create_user_preference_entry(db, 'user_one', 'one@example.com')
    create_user_preference_entry(db, 'user_two', 'two@example.com')
    create_user_preference_entry(db, 'user_three', 'three@example.com')

    found = db_handler.get_entries_by_names(db, ['user_one', 'user_three'])
    assert len(found) == 2
    names = [u.name for u in found]
    assert 'user_one' in names
    assert 'user_three' in names
    assert 'user_two' not in names


def test_get_entries_by_names_empty(db: Session):
    """
    Test that searching for non-existent names returns empty list.
    """
    found = db_handler.get_entries_by_names(db, ['nonexistent1', 'nonexistent2'])
    assert len(found) == 0

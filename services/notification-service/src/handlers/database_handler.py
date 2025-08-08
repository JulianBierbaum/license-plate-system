from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.exceptions.database_exceptions import (
    DatabaseIntegrityError,
    DatabaseQueryError,
    DuplicateEntryError,
    MissingEntryError,
)

from src.models.user_preferences import UserPreferences
from src.schemas.user_preferences import UserPreferencesCreate, UserPreferencesUpdate


def get_entry(db: Session, entry_id: int) -> UserPreferences | None:
    """get user preferences by id

    Args:
        db (Session): db session
        entry_id (int): the id of the entry

    Raises:
        DatabaseQueryError: raised if the query fails

    Returns:
        UserPreferences | None: returns entry object or None
    """
    try:
        stmt = select(UserPreferences).where(UserPreferences.id == entry_id)
        return db.execute(stmt).scalar_one_or_none()
    except SQLAlchemyError as e:
        raise DatabaseQueryError(f"Failed to fetch user preferences: {e}") from e


def get_entry_by_name(db: Session, name: str) -> UserPreferences | None:
    """Retrieve an entry by its name

    Args:
        db (Session): db session
        name (str): name of the user the entry is for

    Raises:
        DatabaseQueryError: raised if the query fails

    Returns:
        UserPreferences | None: returns entry object or None
    """
    try:
        stmt = select(UserPreferences).where(UserPreferences.name == name)
        return db.execute(stmt).scalar_one_or_none()
    except SQLAlchemyError as e:
        raise DatabaseQueryError(f"Failed to fetch user preferences: {e}") from e


def get_entry_by_email(db: Session, email: str) -> UserPreferences | None:
    """Retrieve an entry by its email

    Args:
        db (Session): db session
        email (str): email of the user the entry is for

    Raises:
        DatabaseQueryError: raised if the query fails

    Returns:
        UserPreferences | None: returns entry object or None
    """
    try:
        stmt = select(UserPreferences).where(UserPreferences.email == email)
        return db.execute(stmt).scalar_one_or_none()
    except SQLAlchemyError as e:
        raise DatabaseQueryError(f"Failed to fetch user preferences: {e}") from e


def get_entries(db: Session) -> list[UserPreferences]:
    """get preferences for all users

    Args:
        db (Session): db session

    Raises:
        DatabaseQueryError: raised if the query failes

    Returns:
        list[UserPreferences]: returns list of entries
    """
    try:
        stmt = select(UserPreferences)
        return db.execute(stmt).scalars().all()
    except SQLAlchemyError as e:
        raise DatabaseQueryError(f"Failed to fetch preferences for all users: {e}") from e


def create_new_entry(db: Session, entry: UserPreferencesCreate) -> UserPreferences:
    """creates a new database entry of the UserPreference object

    Args:
        db (Session): db session
        entry (UserPreferencesCreate): entry object to insert

    Raises:
        DuplicateEntryError: raised when an entry with the same name already existy
        DatabaseQueryError: raised if the query fails

    Returns:
        UserPreferences: returns the added object
    """
    entry.name = str(entry.name).lower()
    entry.email = str(entry.email).lower()

    if get_entry_by_name(db=db, name=entry.name):
        raise DuplicateEntryError(
            "An entry with the same name already exists in the database"
        )

    if get_entry_by_email(db=db, email=entry.email):
        raise DuplicateEntryError(
            "An entry with the same name already exists in the database"
        )

    db_entry = UserPreferences(
        name=entry.name,
        email=entry.email,
        receive_alerts=entry.receive_alerts,
        receive_updates=entry.receive_updates,
    )
    try:
        db.add(db_entry)
        db.commit()
        db.refresh(db_entry)
        return db_entry
    except SQLAlchemyError as e:
        db.rollback()
        raise DatabaseIntegrityError(f"Failed to add new user entry: {e}") from e


def update_entry(
    db: Session, entry: UserPreferencesUpdate, entry_id: int
) -> UserPreferences:
    """updates an user preferences entry

    Args:
        db (Session): db session
        entry (UserPreferencesUpdate): the updated values
        entry_id (int): the id of the object to update

    Raises:
        MissingEntryError: raied if no entry with the specified id exists
        DuplicateEntryError: raied when an entry with the same name already exits

    Returns:
        UserPreferences: returns the added object
    """
    db_entry = get_entry(db=db, entry_id=entry_id)
    if not db_entry:
        raise MissingEntryError("No entry with the specified id found")

    entry.name = str(entry.name).lower()
    entry.email = str(entry.email).lower()

    if get_entry_by_name(db=db, name=entry.name) and db_entry.name != entry.name:
        raise DuplicateEntryError(
            "An entry with the same name already exists in the database"
        )

    if get_entry_by_email(db=db, email=entry.email) and db_entry.email != entry.email:
        raise DuplicateEntryError(
            "An entry with the same name already exists in the database"
        )

    try:
        update_data = entry.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_entry, key, value)

        db.commit()
        db.refresh(db_entry)
        return db_entry
    except SQLAlchemyError as e:
        db.rollback()
        raise DatabaseIntegrityError(f"Failed to update user entry: {e}") from e

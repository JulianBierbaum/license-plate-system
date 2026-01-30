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
        raise DatabaseQueryError(f'Failed to fetch user preferences: {e}') from e


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
        raise DatabaseQueryError(f'Failed to fetch user preferences: {e}') from e


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
        raise DatabaseQueryError(f'Failed to fetch user preferences: {e}') from e


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
        raise DatabaseQueryError(f'Failed to fetch preferences for all users: {e}') from e


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
    entry.email = str(entry.email).lower()

    if get_entry_by_email(db=db, email=entry.email):
        raise DuplicateEntryError('An entry with the same email already exists in the database')

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
        raise DatabaseIntegrityError(f'Failed to add new user entry: {e}') from e


def update_entry(db: Session, entry: UserPreferencesUpdate, entry_id: int) -> UserPreferences:
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
        raise MissingEntryError('No entry with the specified id found')

    update_data = entry.model_dump(exclude_unset=True)

    if 'email' in update_data and update_data['email']:
        update_data['email'] = str(update_data['email']).lower()
        if get_entry_by_email(db=db, email=update_data['email']) and db_entry.email != update_data['email']:
            raise DuplicateEntryError('An entry with the same email already exists in the database')

    for key, value in update_data.items():
        setattr(db_entry, key, value)

    try:
        db.commit()
        db.refresh(db_entry)
        return db_entry
    except SQLAlchemyError as e:
        db.rollback()
        raise DatabaseIntegrityError(f'Failed to update user entry: {e}') from e


def delete_entry(db: Session, entry_id: int) -> bool:
    """Delete a user preferences entry

    Args:
        db (Session): db session
        entry_id (int): the id of the entry to delete

    Raises:
        MissingEntryError: raised if no entry with the specified id exists
        DatabaseIntegrityError: raised if the delete fails

    Returns:
        bool: True if deletion was successful
    """
    db_entry = get_entry(db=db, entry_id=entry_id)
    if not db_entry:
        raise MissingEntryError('No entry with the specified id found')

    try:
        db.delete(db_entry)
        db.commit()
        return True
    except SQLAlchemyError as e:
        db.rollback()
        raise DatabaseIntegrityError(f'Failed to delete user entry: {e}') from e


def get_entries_by_preference(
    db: Session, receive_alerts: bool | None = None, receive_updates: bool | None = None
) -> list[UserPreferences]:
    """Get user preferences filtered by notification preferences

    Args:
        db (Session): db session
        receive_alerts (bool | None): filter by receive_alerts preference
        receive_updates (bool | None): filter by receive_updates preference

    Raises:
        DatabaseQueryError: raised if the query fails

    Returns:
        list[UserPreferences]: list of matching entries
    """
    try:
        stmt = select(UserPreferences)

        if receive_alerts is not None:
            stmt = stmt.where(UserPreferences.receive_alerts == receive_alerts)

        if receive_updates is not None:
            stmt = stmt.where(UserPreferences.receive_updates == receive_updates)

        return db.execute(stmt).scalars().all()
    except SQLAlchemyError as e:
        raise DatabaseQueryError(f'Failed to fetch user preferences by preference: {e}') from e


def get_entries_by_names(db: Session, names: list[str]) -> list[UserPreferences]:
    """Get user preferences for specific users by name

    Args:
        db (Session): db session
        names (list[str]): list of user names to find

    Raises:
        DatabaseQueryError: raised if the query fails

    Returns:
        list[UserPreferences]: list of matching entries
    """
    try:
        # Normalize names to lowercase for comparison
        stmt = select(UserPreferences).where(UserPreferences.name.in_(names))
        return db.execute(stmt).scalars().all()
    except SQLAlchemyError as e:
        raise DatabaseQueryError(f'Failed to fetch user preferences by names: {e}') from e

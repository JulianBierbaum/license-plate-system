from fastapi import APIRouter, HTTPException, status

from src.db.session import SessionDep
import src.handlers.database_handler as crud
from src.exceptions.database_exceptions import (
    DatabaseIntegrityError,
    DatabaseQueryError,
    DuplicateEntryError,
    MissingEntryError,
)
import src.schemas.user_preferences as  schemas

router = APIRouter()


@router.post("/", response_model=schemas.UserPreference)
def create_user_preferences(db: SessionDep, entry: schemas.UserPreferencesCreate):
    """
    Create new user preferences.

    Args:
        db (SessionDep): Database session dependency
        entry (schemas.UserPreferencesCreate): User preferences data to create

    Returns:
        schemas.UserPreference: Newly created user preferences record
    """
    try:
        return crud.create_new_entry(db=db, entry=entry)
    except DuplicateEntryError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User preferences with this name already exist",
        )
    except DatabaseIntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Database integrity error: {e}",
        )


@router.get("/", response_model=list[schemas.UserPreference])
def get_all_user_preferences(db: SessionDep):
    """
    Retrieve all user preferences records.

    Args:
        db (SessionDep): Database session dependency

    Returns:
        List[schemas.UserPreference]: List of all user preferences records
    """
    try:
        return crud.get_entries(db=db)
    except DatabaseQueryError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch user preferences",
        )


@router.get("/{entry_id}", response_model=schemas.UserPreference)
def get_user_preferences_by_id(db: SessionDep, entry_id: int):
    """
    Retrieve user preferences by ID.

    Args:
        db (SessionDep): Database session dependency
        entry_id (int): ID of user preferences to retrieve

    Returns:
        schemas.UserPreference: Requested user preferences record
        HTTP 404 Not Found: If no user preferences found with specified ID
    """
    try:
        entry = crud.get_entry(db=db, entry_id=entry_id)
        if not entry:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User preferences not found",
            )
        return entry
    except DatabaseQueryError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch user preferences",
        )


@router.get("/by-name/{name}", response_model=schemas.UserPreference)
def get_user_preferences_by_name(db: SessionDep, name: str):
    """
    Retrieve user preferences by name.

    Args:
        db (SessionDep): Database session dependency
        name (str): Name of user to retrieve preferences for

    Returns:
        schemas.UserPreference: Requested user preferences record
        HTTP 404 Not Found: If no user preferences found with specified name
    """
    try:
        entry = crud.get_entry_by_name(db=db, name=name)
        if not entry:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User preferences not found",
            )
        return entry
    except DatabaseQueryError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch user preferences",
        )


@router.put("/{entry_id}", response_model=schemas.UserPreference)
def update_user_preferences(
    db: SessionDep, entry_id: int, entry: schemas.UserPreferencesUpdate
):
    """
    Update user preferences by ID.

    Args:
        db (SessionDep): Database session dependency
        entry_id (int): ID of user preferences to update
        entry (schemas.UserPreferencesUpdate): Updated user preferences data

    Returns:
        schemas.UserPreference: Updated user preferences record
    """
    try:
        return crud.update_entry(db=db, entry=entry, entry_id=entry_id)
    except MissingEntryError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User preferences not found",
        )
    except DuplicateEntryError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User preferences with this name already exist",
        )
    except DatabaseIntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Database integrity error: {e}",
        )
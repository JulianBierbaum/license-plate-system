from datetime import datetime

from pydantic import BaseModel, Field, EmailStr


class UserPreferencesBase(BaseModel):
    """user preferences base model"""

    name: str = Field(..., min_length=5, max_length=50)
    email: EmailStr = Field(..., min_length=5, max_length=50)
    receive_alerts: bool = False
    receive_updates: bool = False


class UserPreferencesCreate(UserPreferencesBase):
    """ "schema for creating a new user preferences entry"""

    pass


class UserPreferencesUpdate(UserPreferencesBase):
    """ "schema for updating a user preferences entry"""

    name: str | None = None
    email: EmailStr | None = None
    receive_alerts: bool | None = None
    receive_updates: bool | None = None


class UserPreferenceInDB(UserPreferencesBase):
    """ "schema for db representation of user preferences"""

    id: int
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


class UserPreference(UserPreferenceInDB):
    """user preferences representation schema"""

    pass

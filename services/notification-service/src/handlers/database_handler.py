from datetime import datetime, timedelta
from hashlib import sha256
from typing import Any

from sqlalchemy import and_
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from src.exceptions.database_exceptions import (
    DatabaseIntegrityError,
    DatabaseQueryError,
)
from src.logger import logger
from src.models.user_preferences import UserPreferences
from src.schemas.user_preferences import (
    UserPreference,
    UserPreferencesCreate,
    UserPreferencesUpdate
)


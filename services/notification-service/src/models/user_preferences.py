from sqlalchemy import Column, DateTime, Integer, String, Boolean, text
from sqlalchemy.sql import func

# relative imports needed for db-prestart service
from ..models.base import NotificationBase


class UserPreferences(NotificationBase):
    """SQLAlchemy model for the user preferences objects

    Args:
        NotificationBase (postgres schema): base for the notification schema
    """

    __tablename__ = 'user_preferences'

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )
    name = Column(
        String(50),
        unique=True,
        index=True,
        nullable=False,
    )
    email = Column(
        String(50),
        unique=True,
        nullable=False,
    )
    receive_alerts = Column(
        Boolean,
        nullable=False,
        index=True,
        server_default=text('false'),
    )
    receive_updates = Column(
        Boolean,
        nullable=False,
        index=True,
        server_default=text('false'),
    )
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=True,
        server_onupdate=func.now(),
    )

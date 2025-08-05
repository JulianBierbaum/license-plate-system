from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base

from ..config import settings

notification_metadata = MetaData(schema=settings.notification_schema)

NotificationBase = declarative_base(metadata=notification_metadata)

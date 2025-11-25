from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base
import os

notification_metadata = MetaData(schema=os.getenv('NOTIFICATION_SCHEMA'))

NotificationBase = declarative_base(metadata=notification_metadata)

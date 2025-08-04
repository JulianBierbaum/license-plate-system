from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base

from ..config import settings

ingestion_metadata = MetaData(schema=settings.data_collection_schema)

IngestionBase = declarative_base(metadata=ingestion_metadata)

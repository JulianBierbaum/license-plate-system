import os

from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base

ingestion_metadata = MetaData(schema=os.getenv('DATA_COLLECTION_SCHEMA'))

IngestionBase = declarative_base(metadata=ingestion_metadata)

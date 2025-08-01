from sqlalchemy import MetaData
from sqlalchemy.orm import declarative_base

ingestion_metadata = MetaData(schema="ingestion_schema")

IngestionBase = declarative_base(metadata=ingestion_metadata)

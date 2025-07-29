from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base

ingestion_metadata = MetaData(schema="ingestion_schema")

IngestionBase = declarative_base(metadata=ingestion_metadata)

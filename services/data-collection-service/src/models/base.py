from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base

# Service-specific base - no sharing
metadata = MetaData(schema="ingestion_schema")
Base = declarative_base(metadata=metadata)

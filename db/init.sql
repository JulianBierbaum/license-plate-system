-- Create users with environment variable passwords
CREATE USER notification_user WITH PASSWORD :NOTIFICATION_DB_PASSWORD;
CREATE USER data_collection_user WITH PASSWORD :DATA_COLLECTION_DB_PASSWORD;
CREATE USER analytics_user WITH PASSWORD :ANALYTICS_DB_PASSWORD;

-- Grant database connection privileges
GRANT CONNECT ON DATABASE :DB_NAME TO data_collection_user;
GRANT CONNECT ON DATABASE :DB_NAME TO analytics_user;
GRANT CONNECT ON DATABASE :DB_NAME TO notification_user;

-- Create schemas
CREATE SCHEMA IF NOT EXISTS ingestion_schema;
CREATE SCHEMA IF NOT EXISTS analytics_schema;
CREATE SCHEMA IF NOT EXISTS notification_schema;

-- Set up Data Collection Service permissions (writes to ingestion_schema)
GRANT ALL ON SCHEMA ingestion_schema TO data_collection_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA ingestion_schema TO data_collection_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA ingestion_schema TO data_collection_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA ingestion_schema GRANT ALL ON TABLES TO data_collection_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA ingestion_schema GRANT ALL ON SEQUENCES TO data_collection_user;

-- Set up Analytics Service permissions (reads from ingestion_schema, writes to analytics_schema)
GRANT USAGE ON SCHEMA ingestion_schema TO analytics_user;
GRANT SELECT ON ALL TABLES IN SCHEMA ingestion_schema TO analytics_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA ingestion_schema GRANT SELECT ON TABLES TO analytics_user;

GRANT ALL ON SCHEMA analytics_schema TO analytics_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA analytics_schema TO analytics_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA analytics_schema TO analytics_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA analytics_schema GRANT ALL ON TABLES TO analytics_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA analytics_schema GRANT ALL ON SEQUENCES TO analytics_user;

-- Set up notification Service permissions (writes to notification_schema)
GRANT ALL ON SCHEMA notification_schema TO notification_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA notification_schema TO notification_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA notification_schema TO notification_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA notification_schema GRANT ALL ON TABLES TO notification_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA notification_schema GRANT ALL ON SEQUENCES TO notification_user;

-- Set search paths for each user
ALTER ROLE data_collection_user SET search_path = ingestion_schema,public;
ALTER ROLE analytics_user SET search_path = analytics_schema,ingestion_schema,public;
ALTER ROLE notification_user SET search_path = notification_schema,public;
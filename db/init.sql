-- Create users with environment variable passwords
CREATE USER notification_user WITH PASSWORD :'NOTIFICATION_DB_PASSWORD';
CREATE USER data_collection_user WITH PASSWORD :'DATA_COLLECTION_DB_PASSWORD';
CREATE USER analytics_user WITH PASSWORD :'ANALYTICS_DB_PASSWORD';

-- Create schemas
CREATE SCHEMA IF NOT EXISTS notifications;
CREATE SCHEMA IF NOT EXISTS data_collection;
CREATE SCHEMA IF NOT EXISTS analytics;

-- Grant privileges
GRANT ALL ON SCHEMA notifications TO notification_user;
GRANT ALL ON SCHEMA data_collection TO data_collection_user;
GRANT ALL ON SCHEMA analytics TO analytics_user;

-- Grant usage on schemas
GRANT USAGE ON SCHEMA notifications TO notification_user;
GRANT USAGE ON SCHEMA data_collection TO data_collection_user;
GRANT USAGE ON SCHEMA analytics TO analytics_user;

-- Grant permissions on future tables
ALTER DEFAULT PRIVILEGES IN SCHEMA notifications GRANT ALL ON TABLES TO notification_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA data_collection GRANT ALL ON TABLES TO data_collection_user;
ALTER DEFAULT PRIVILEGES IN SCHEMA analytics GRANT ALL ON TABLES TO analytics_user;

-- Set search paths
ALTER ROLE notification_user SET search_path = notifications,public;
ALTER ROLE data_collection_user SET search_path = data_collection,public;
ALTER ROLE analytics_user SET search_path = analytics,public;
#!/bin/bash
set -e

echo "Waiting for PostgreSQL to be ready..."
until pg_isready -h $DB_HOST -p $DB_PORT -U $DB_USER; do
  echo "PostgreSQL is unavailable - sleeping"
  sleep 1
done

echo "PostgreSQL is up - executing commands"

echo "Creating users and schemas..."
PGPASSWORD=$DB_PASSWORD psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME \
  -v NOTIFICATION_DB_PASSWORD="'$NOTIFICATION_DB_PASSWORD'" \
  -v DATA_COLLECTION_DB_PASSWORD="'$DATA_COLLECTION_DB_PASSWORD'" \
  -v ANALYTICS_DB_PASSWORD="'$ANALYTICS_DB_PASSWORD'" \
  -v DB_NAME="$DB_NAME" \
  -f /app/init.sql

echo "Running migrations..."
alembic upgrade head


echo "Database setup complete!"

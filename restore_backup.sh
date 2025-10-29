#!/bin/bash

# PostgreSQL Restore Script for License Plate System
# Usage: ./restore_backup.sh <PATH_TO_BACKUP_FILE>

set -e

# Check if a backup file path is provided as an argument
if [ -z "$1" ]; then
    echo "Usage: $0 <path_to_backup_file>"
    echo "Example: $0 backups/your_database_manual_20231027_103000.dump.gz"
    exit 1
fi

BACKUP_FILE="$1"

# Check if the specified backup file actually exists
if [ ! -f "$BACKUP_FILE" ]; then
    echo "Error: Backup file '$BACKUP_FILE' not found."
    exit 1
fi

# Load environment variables from the .env file
if [ -f ".env" ]; then
    set -a
    source ".env"
    set +a
else
    echo "Error: .env file not found. Please run this script from the project root."
    exit 1
fi

# Find the running PostgreSQL container
POSTGRES_CONTAINER=$(docker compose ps -q postgres)
if [ -z "$POSTGRES_CONTAINER" ]; then
    echo "Error: PostgreSQL container not found. Is it running? (Hint: docker compose up -d)"
    exit 1
fi

echo "Preparing to restore database..."
echo "   Database:  $DB_NAME"
echo "   Container: $POSTGRES_CONTAINER"
echo "   Source File: $BACKUP_FILE"
echo "----------------------------------------"

read -p "This will completely ERASE and REPLACE the current database. Are you sure? (y/N): " -n 1 -r
echo

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Restore cancelled by user."
    exit 0
fi

echo "Stopping dependent services..."

docker compose stop analytics-service data-collection-service notification-service postgres-backup

sleep 5

echo "Terminating any remaining database connections..."

# Terminate connections to database
docker exec "$POSTGRES_CONTAINER" psql -U "$POSTGRES_ADMIN_USER" -d postgres -c "
SELECT pg_terminate_backend(pg_stat_activity.pid)
FROM pg_stat_activity
WHERE pg_stat_activity.datname = '$DB_NAME'
  AND pid <> pg_backend_pid();"

echo "Dropping and recreating the database..."

# Drop the existing database
docker exec "$POSTGRES_CONTAINER" dropdb -U "$POSTGRES_ADMIN_USER" --if-exists "$DB_NAME"

# Create database
docker exec "$POSTGRES_CONTAINER" createdb -U "$POSTGRES_ADMIN_USER" "$DB_NAME"

echo "Restoring database from backup. This may take a moment..."

if gunzip -c "$BACKUP_FILE" | docker exec -i "$POSTGRES_CONTAINER" pg_restore \
    -U "$POSTGRES_ADMIN_USER" \
    -d "$DB_NAME" \
    --verbose \
    --clean \
    --if-exists \
    --no-owner \
    --no-privileges
then
    echo "Database restore successful!"
else
    echo "Database restore failed!"
    exit 1
fi

echo "You can now restart the services."

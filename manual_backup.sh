#!/bin/bash

# PostgreSQL Backup Script for License Plate System (Docker-based)
# Usage: ./backup.sh <DB_HOST> [DB_PORT]

set -e

# Check args
if [ -z "$1" ]; then
    echo "Usage: $0 <db_host> [db_port]"
    exit 1
fi

if [ -f ".env" ]; then
    set -a
    source ".env"
    set +a
else
    echo "Error: .env file not found in project root."
    exit 1
fi

DB_HOST="$1"
DB_PORT="${3:-5432}"

# map localhost -> host.docker.internal
if [ "$DB_HOST" = "localhost" ] || [ "$DB_HOST" = "127.0.0.1" ]; then
    DB_HOST="host.docker.internal"
    echo "Note: Using host.docker.internal to reach local database from inside container."
fi

if [ -z "$DB_NAME" ] || [ -z "$POSTGRES_ADMIN_USER" ] || [ -z "$POSTGRES_ADMIN_PASSWORD" ]; then
    echo "Error: DB_NAME or POSTGRES_ADMIN_USER or POSTGRES_ADMIN_PASSWORD missing in .env file."
    exit 1
fi

# Ensure backup directory exists
mkdir -p "$BACKUP_DIR"

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/${DB_NAME}_manual_${TIMESTAMP}.dump"

echo "=== Starting backup ==="
echo "Host: $DB_HOST"
echo "Port: $DB_PORT"
echo "Database: $DB_NAME"
echo "Backup file: $BACKUP_FILE"
echo "======================="

# Run pg_dump inside temporary container
docker run --rm -i \
    --add-host=host.docker.internal:host-gateway \
    -e PGPASSWORD="$POSTGRES_ADMIN_PASSWORD" \
    -v "$(pwd)":/backup \
    postgres:14-alpine bash -c "
        echo 'Running backup...';
        pg_dump \
            -h '$DB_HOST' \
            -p '$DB_PORT' \
            -U '$POSTGRES_ADMIN_USER' \
            -d '$DB_NAME' \
            --verbose \
            --clean \
            --no-owner \
            --no-privileges \
            --format=custom > /backup/$BACKUP_FILE
    "

# Compress backup
gzip "$BACKUP_FILE"
BACKUP_FILE_FINAL="${BACKUP_FILE}.gz"
BACKUP_SIZE=$(du -h "$BACKUP_FILE_FINAL" | cut -f1)

echo "Backup completed successfully!"
echo "   File: $BACKUP_FILE_FINAL"
echo "   Size: $BACKUP_SIZE"

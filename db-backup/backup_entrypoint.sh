#!/bin/sh

# Dockerized PostgreSQL Backup Script for License Plate System
# This script runs inside the postgres-backup container

set -e

DB_HOST=${DB_HOST}
DB_PORT=${DB_PORT}
DB_USER=${DB_USER}
DB_PASSWORD=${DB_PASSWORD}
DB_NAME=${DB_NAME}
BACKUP_RETENTION_DAYS=${BACKUP_RETENTION_DAYS}

# Backup directory
BACKUP_DIR="/backups"

# Ensure backup directory exists
mkdir -p "$BACKUP_DIR"

# Generate backup filename
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="${BACKUP_DIR}/${DB_NAME}_automated_${TIMESTAMP}.dump"

echo "=== Starting automatied backup ==="
echo "Database: $DB_NAME"
echo "Container: $POSTGRES_CONTAINER"
echo "Backup file: $BACKUP_FILE"
echo "Retention: $BACKUP_RETENTION_DAYS day(s)"
echo "================================="

# Wait for PostgreSQL to be ready
echo "Checking database connectivity..."
until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME"; do
    echo "Waiting for database to be ready..."
    sleep 5
done

echo "Database is ready, starting backup..."

# Set password for pg_dump
export PGPASSWORD="$DB_PASSWORD"

# Create backup
if pg_dump \
    -h "$DB_HOST" \
    -p "$DB_PORT" \
    -U "$DB_USER" \
    -d "$DB_NAME" \
    --verbose \
    --clean \
    --no-owner \
    --no-privileges \
    --format=custom > "$BACKUP_FILE"
then
    # Compress the backup
    gzip "$BACKUP_FILE"
    BACKUP_FILE_FINAL="${BACKUP_FILE}.gz"

    # Get file size
    BACKUP_SIZE=$(du -h "$BACKUP_FILE_FINAL" | cut -f1)

    echo "Backup successful:"
    echo "   File: $BACKUP_FILE_FINAL"
    echo "   Size: $BACKUP_SIZE"

    # Remove old backups
    echo "Removing backups older than ${BACKUP_RETENTION_DAYS} days..."
    find "$BACKUP_DIR" -name "${DB_NAME}_automated_*.dump.gz" -type f -mtime +${BACKUP_RETENTION_DAYS} -delete
    echo "Cleanup completed"
else
    echo "Backup failed!"
    exit 1
fi

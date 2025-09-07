#!/bin/bash

# Manual PostgreSQL Backup Script for License Plate System
# Usage: ./backup.sh <BACKUP_NAME>

set -e

# Load environment variables from .env file
if [ -f ".env" ]; then
    set -a
    source ".env"
    set +a
else
    echo "Error: .env file not found in project root"
    exit 1
fi

BACKUP_DIR="${BACKUP_DIR}"

# Ensure backup directory exists
mkdir -p "$BACKUP_DIR"

# Find running PostgreSQL container
POSTGRES_CONTAINER=$(docker compose ps -q postgres)
if [ -z "$POSTGRES_CONTAINER" ]; then
    echo "Error: PostgreSQL container not found. Is it running?"
    exit 1
fi

# Generate backup filename with timestamp
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="$BACKUP_DIR/${DB_NAME}_manual_${TIMESTAMP}.dump"

echo "=== Starting manual backup ==="
echo "Database: $DB_NAME"
echo "Container: $POSTGRES_CONTAINER"
echo "Backup file: $BACKUP_FILE"
echo "================================="

# Create backup
if docker exec "$POSTGRES_CONTAINER" pg_dump \
    -U "$POSTGRES_ADMIN_USER" \
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

    BACKUP_SIZE=$(du -h "$BACKUP_FILE_FINAL" | cut -f1)

    echo "Backup successful:"
    echo "   File: $BACKUP_FILE_FINAL"
    echo "   Size: $BACKUP_SIZE"
else
    echo "Backup failed!"
    exit 1
fi

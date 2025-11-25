#!/bin/bash

# PostgreSQL Restore Script for License Plate System (Docker-based)
# Usage: ./restore_backup.sh <PATH_TO_BACKUP_FILE> <DB_HOST> [DB_PORT]

set -e

# check args
if [ -z "$1" ] || [ -z "$2" ]; then
    echo "Usage: $0 <path_to_backup_file> <db_host> [db_port]"
    exit 1
fi

if [ -f ".env" ]; then
    set -a
    source ".env"
    set +a
else
    echo "Error: .env file not found. Please run this script from the project root."
    exit 1
fi

BACKUP_FILE="$1"
DB_HOST="$2"
DB_PORT="${3:-5432}"

# map localhost -> host.docker.internal
if [ "$DB_HOST" = "localhost" ] || [ "$DB_HOST" = "127.0.0.1" ]; then
    DB_HOST="host.docker.internal"
    echo "Note: Using host.docker.internal to reach local database from inside container."
fi

if [ -z "$DB_NAME" ] || [ -z "$POSTGRES_ADMIN_USER" ]; then
    echo "Error: DB_NAME or POSTGRES_ADMIN_USER missing in .env file."
    exit 1
fi

if [ ! -f "$BACKUP_FILE" ]; then
    echo "Error: Backup file '$BACKUP_FILE' not found."
    exit 1
fi

echo "=== Preparing restore... ==="
echo "Host: $DB_HOST"
echo "Port: $DB_PORT"
echo "Database: $DB_NAME"
echo "Backup file: $BACKUP_FILE"
echo "============================"

read -p "This will completely ERASE and REPLACE the current database. Are you sure? (y/N): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Restore cancelled by user."
    exit 0
fi

# Docker db client
echo "Starting temporary PostgreSQL client container..."

docker run --rm -i \
    --add-host=host.docker.internal:host-gateway \
    -e PGPASSWORD="$POSTGRES_ADMIN_PASSWORD" \
    -v "$(pwd)":/backup \
    postgres:14-alpine bash -c "
        echo 'Terminating active connections...';
        psql -h '$DB_HOST' -p '$DB_PORT' -U '$POSTGRES_ADMIN_USER' -d postgres -c \"
        SELECT pg_terminate_backend(pg_stat_activity.pid)
        FROM pg_stat_activity
        WHERE pg_stat_activity.datname = '$DB_NAME'
          AND pid <> pg_backend_pid();
        \" || true

        echo 'Dropping database...';
        dropdb -h '$DB_HOST' -p '$DB_PORT' -U '$POSTGRES_ADMIN_USER' --if-exists '$DB_NAME';

        echo 'Creating database...';
        createdb -h '$DB_HOST' -p '$DB_PORT' -U '$POSTGRES_ADMIN_USER' '$DB_NAME';

        echo 'Restoring backup...';
        gunzip -c /backup/$BACKUP_FILE | pg_restore \
            -h '$DB_HOST' \
            -p '$DB_PORT' \
            -U '$POSTGRES_ADMIN_USER' \
            -d '$DB_NAME' \
            --verbose \
            --clean \
            --if-exists \
            --no-owner \
            --no-privileges;
    "

echo "Database restore completed successfully!"

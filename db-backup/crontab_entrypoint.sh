#!/bin/sh

# This script starts the cron job for the automatic backups
# This script runs inside the postgres-backup container

set -e

SCHEDULE="${BACKUP_SCHEDULE}"

if [ -z "$BACKUP_SCHEDULE" ]; then
    echo "Automatic backups disabled. Container will idle."
    tail -f /dev/null
fi

echo "Using backup schedule: ${SCHEDULE}"

# Create crontab
echo "${SCHEDULE} /backup-entrypoint.sh >> /var/log/cron.log 2>&1" > /var/spool/cron/crontabs/root

# Ensure proper permissions
chmod 0644 /var/spool/cron/crontabs/root

echo "Starting backup job..."
exec crond -f -l 2

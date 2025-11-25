#!/bin/sh
set -e

SCHEDULE="${BACKUP_SCHEDULE}"

if [ -z "$SCHEDULE" ]; then
    echo "Automatic backups disabled. Container will idle."
    tail -f /dev/null
fi

echo "Using backup schedule: ${SCHEDULE}"

echo "${SCHEDULE} /backup_entrypoint.sh >> /var/log/cron.log 2>&1" > /var/spool/cron/crontabs/root

# Ensure proper permissions
chmod 0644 /var/spool/cron/crontabs/root

echo "Starting cron daemon..."

# Start cron in foreground so container doesn't exit
crond -f -l 8

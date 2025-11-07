# Monitoring

## Health Checks

The following services have health checks configured in the `docker-compose.yaml` files:

-   **PostgreSQL Database (`postgres`)**:
    -   A health check is performed to ensure that the PostgreSQL database is ready to accept connections.
    -   The command used is `pg_isready -U ${POSTGRES_ADMIN_USER} -d ${DB_NAME}`.
    -   It runs every 5 seconds with a 5-second timeout and 5 retries.

-   **Plate Recognizer (`plate-recognizer`)**:
    -   A health check is performed to ensure that the Plate Recognizer service is running.
    -   The command used is `curl -f http://localhost:8080/`.
    -   It runs every 5 seconds with a 5-second timeout and 5 retries.

-   **Data Collection Service (`data-collection-service`)**:
    -   A health check is performed to ensure that the Data Collection service is running.
    -   The command used is `curl -f http://localhost:5000/health`.
    -   It runs every 5 seconds with a 5-second timeout and 5 retries.

-   **Notification Service (`notification-service`)**:
    -   A health check is performed to ensure that the Notification service is running.
    -   The command used is `curl -f http://localhost:5000/health`.
    -   It runs every 5 seconds with a 5-second timeout and 5 retries.

-   **Database Backup Service (`db-backup`)**:
    -   A health check is performed to ensure that the cron daemon is running.
    -   The command used is `pgrep crond || exit 1`.
    -   It runs every 5 seconds with a 5-second timeout and 5 retries.

## Logging

All services are configured to output logs to the console. The log level can be configured via the `LOG_LEVEL` environment variable in the `.env` file.
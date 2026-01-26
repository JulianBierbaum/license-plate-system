# Configuration

The system is configured using environment variables. These variables are stored in a `.env` file in the root of the project.

## Global

*   `LOG_LEVEL`: The log level for all services. Defaults to `DEBUG` in development and can be set to `INFO`, `WARNING`, `ERROR`, or `CRITICAL` in production.
*   `DOCKER_REGISTRY`: The Docker registry to push images to. Used by the `build.sh` script.

## Database (PostgreSQL)

*   `DB_HOST`: The hostname of the PostgreSQL database.
*   `DB_PORT`: The port of the PostgreSQL database.
*   `DB_PORT_EXTERNAL`: The external port to map to the PostgreSQL container.
*   `DB_NAME`: The name of the database.
*   `POSTGRES_ADMIN_USER`: The username for the PostgreSQL superuser.
*   `POSTGRES_ADMIN_PASSWORD`: The password for the PostgreSQL superuser.

## Services

### Analytics Service

*   `ANALYTICS_DB_USER`: The username for the analytics service to connect to the database.
*   `ANALYTICS_DB_PASSWORD`: The password for the analytics service to connect to the database.
*   `ANALYTICS_SCHEMA`: The database schema for the analytics service.

### Auth Service

*   `ACTIVE_DIRECTORY_URL`: The URL of the Active Directory server for authentication.

### Data Collection Service

*   `DATA_COLLECTION_DB_USER`: The username for the data collection service to connect to the database.
*   `DATA_COLLECTION_DB_PASSWORD`: The password for the data collection service to connect to the database.
*   `DATA_COLLECTION_SCHEMA`: The database schema for the data collection service.
*   `SYNOLOGY_HOST`: The hostname of the Synology NAS.
*   `SYNOLOGY_USERNAME`: The username for the Synology NAS.
*   `SYNOLOGY_PASSWORD`: The password for the Synology NAS.
*   `PLATE_RECOGNIZER_API_KEY`: The API key for the Plate Recognizer service.
*   `SAVE_IMAGES_FOR_DEBUG`: Whether to save images for debugging purposes.
*   `INTERVAL_SECONDS`: The interval in seconds to poll the Synology NAS for new images.
*   `PLATE_RECOGNIZER_SERVICE_URL`: The URL of the Plate Recognizer service.
*   `SAVE_DIR`: The directory to save snapshots to.

### Notification Service

*   `NOTIFICATION_DB_USER`: The username for the notification service to connect to the database.
*   `NOTIFICATION_DB_PASSWORD`: The password for the notification service to connect to the database.
*   `NOTIFICATION_SCHEMA`: The database schema for the notification service.
*   `ANALYTICS_SERVICE_URL`: The URL of the analytics service.
*   `SENDER_ADDRESS`: The email address to send notifications from.
*   `SMTP_RELAY_ADDRESS`: The IP address of the SMTP open mail relay.
*   `SMTP_PORT`: The SMTP port (optional, defaults to 25).
*   `NOTIFICATION_API_KEY`: API key for authenticating requests to the notification service.

### Web Service

*   `AUTH_SERVICE_URL`: The URL of the auth service.
*   `ANALYTICS_SERVICE_URL`: The URL of the analytics service.
*   `NOTIFICATION_SERVICE_URL`: The URL of the notification service.

### Plate Recognizer Service

*   `LICENSE_KEY`: The license key for the Plate Recognizer service.

## Backup

*   `BACKUP_DIR`: The directory to save backups to.
*   `BACKUP_RETENTION_DAYS`: The number of days to retain automatic backups.
*   `BACKUP_SCHEDULE`: The cron schedule for automatic backups.

## Grafana

*   `GRAFANA_ADMIN_USER`: The username for Grafana administrative access.
*   `GRAFANA_ADMIN_PASSWORD`: The password for Grafana administrative access.
*   `GRAFANA_PORT_EXTERNAL`: The external port for Grafana access.

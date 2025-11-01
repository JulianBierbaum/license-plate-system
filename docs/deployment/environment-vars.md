# Production Environment Variables

This section provides information about the environment variables required for a production deployment.

## Comprehensive List of Variables

A comprehensive list of all environment variables used in the project can be found in the [Configuration](../getting-started/configuration.md) guide. The same variables are used in both development and production, but their values will differ.

## Production-Specific Considerations

When configuring the environment variables for a production deployment, please pay special attention to the following:

*   **`LOG_LEVEL`**: Set this to `INFO` or `WARNING` for production to avoid excessive logging.
*   **Database Credentials**: Use strong, unique passwords for `POSTGRES_ADMIN_PASSWORD` and all the service-specific database passwords (`ANALYTICS_DB_PASSWORD`, `DATA_COLLECTION_DB_PASSWORD`, `NOTIFICATION_DB_PASSWORD`).
*   **`ACTIVE_DIRECTORY_URL`**: Ensure this points to your production Active Directory server.
*   **`SYNOLOGY_HOST`**: This should be the hostname or IP address of your production Synology NAS.
*   **`PLATE_RECOGNIZER_API_KEY` and `LICENSE_KEY`**: Use your production license keys for the Plate Recognizer service.
*   **Service URLs**: The service URLs (`ANALYTICS_SERVICE_URL`, `NOTIFICATION_SERVICE_URL`, `AUTH_SERVICE_URL`) should point to the correct locations in your production environment. If you are using the provided `docker-compose.prod.yaml` file, the default values should be correct.
*   **`SENDER_ADDRESS`**: This should be a valid email address that you want to use for sending notifications in production.
*   **`BACKUP_SCHEDULE`**: Configure a suitable cron schedule for your production database backups.
*   **`BACKUP_RETENTION_DAYS`**: Set a reasonable retention period for your backups.

## Security

It is crucial to manage your production environment variables securely. Do not commit your production `.env` file to version control. Use a secure method for managing secrets, such as:

*   A secrets management tool (e.g., HashiCorp Vault, AWS Secrets Manager).
*   Encrypted environment files.
*   The secrets management features of your container orchestrator (e.g., Docker secrets, Kubernetes secrets).

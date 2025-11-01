# Backups

This section describes the backup procedures for the License Plate Recognition System.

## Automatic Backups

The `postgres-backup` service creates periodic backups of the PostgreSQL database. The schedule for these backups is defined by the `BACKUP_SCHEDULE` environment variable, which should be in cron format.

The retention period for automatic backups is controlled by the `BACKUP_RETENTION_DAYS` environment variable. Backups older than this number of days will be automatically deleted.

If the `BACKUP_SCHEDULE` variable is not set, no periodic backups will be performed.

The backups are stored in the directory specified by the `BACKUP_DIR` environment variable.

## Manual Backups

You can perform a manual backup at any time using the `manual_backup.sh` script.

### Usage

```bash
./manual_backup.sh <DB_HOST> [DB_PORT]
```

*   `<DB_HOST>`: The hostname of the database to back up.
*   `[DB_PORT]`: The port of the database. Defaults to `5432`.

### Example

To back up a local database running on the default port:

```bash
./manual_backup.sh localhost
```

The script will create a compressed backup file in the directory specified by the `BACKUP_DIR` environment variable. The filename will be in the format `<DB_NAME>_manual_<TIMESTAMP>.dump.gz`.

### .env File

The `manual_backup.sh` script requires the following environment variables to be set in the `.env` file in the project root:

*   `DB_NAME`
*   `POSTGRES_ADMIN_USER`
*   `POSTGRES_ADMIN_PASSWORD`
*   `BACKUP_DIR`

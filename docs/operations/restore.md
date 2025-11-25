# Restore

This section describes how to restore the database from a backup.

## Using the Restore Script

The `restore_backup.sh` script is used to restore a database backup. This script will completely erase and replace the current database with the data from the backup file.

### Usage

```bash
./restore_backup.sh <PATH_TO_BACKUP_FILE> <DB_HOST> [DB_PORT]
```

*   `<PATH_TO_BACKUP_FILE>`: The path to the backup file to restore.
*   `<DB_HOST>`: The hostname of the database to restore to.
*   `[DB_PORT]`: The port of the database. Defaults to `5432`.

### Example

To restore a backup to a local database running on the default port:

```bash
./restore_backup.sh /path/to/your/backup/file.dump.gz localhost
```

The script will prompt you for confirmation before proceeding, as this is a destructive operation.

### .env File

The `restore_backup.sh` script requires the following environment variables to be set in the `.env` file in the project root:

*   `DB_NAME`
*   `POSTGRES_ADMIN_USER`
*   `POSTGRES_ADMIN_PASSWORD`

## Restore Process

The restore script performs the following steps:

1.  **Terminates active connections:** It disconnects all users from the target database.
2.  **Drops the database:** The existing database is completely deleted.
3.  **Creates a new database:** A new, empty database is created with the same name.
4.  **Restores the backup:** The data from the backup file is imported into the new database.

# Scripts Reference

This section provides a reference for the scripts included in this project.

## `run.sh`

This script is used to start the application in development mode.

*   **Usage:** `./run.sh`
*   **Functionality:**
    *   Starts the Docker containers defined in `docker-compose.dev.yaml`.
    *   Enables hot-reloading for the services, so that changes to the source code are automatically applied.
    *   Sets up a trap to automatically stop and remove the containers when the script is terminated.

## `build.sh`

This script is used to build and push the Docker images for all the services to a Docker registry.

*   **Usage:** `./build.sh`
*   **Functionality:**
    *   Reads the `DOCKER_REGISTRY` environment variable from the `.env` file.
    *   Builds a Docker image for each service in the `services` directory, as well as for `db-prestart`, `db-backup`, and `shared-data`.
    *   Pushes the images to the configured Docker registry.
*   **Prerequisites:**
    *   The `DOCKER_REGISTRY` environment variable must be set.
    *   You must be logged in to the Docker registry (`docker login`).
    *   Lock files (`uv.lock`, `package-lock.json`) must be present.

## `manual_backup.sh`

This script is used to create a manual backup of the PostgreSQL database.

*   **Usage:** `./manual_backup.sh <DB_HOST> [DB_PORT]`
*   **Functionality:**
    *   Connects to the specified database and and creates a compressed backup file.
    *   The backup file is stored in the directory specified by the `BACKUP_DIR` environment variable.
*   **Prerequisites:**
    *   The `.env` file must contain the `DB_NAME`, `POSTGRES_ADMIN_USER`, `POSTGRES_ADMIN_PASSWORD`, and `BACKUP_DIR` variables.

## `restore_backup.sh`

This script is used to restore the PostgreSQL database from a backup file.

*   **Usage:** `./restore_backup.sh <PATH_TO_BACKUP_FILE> <DB_HOST> [DB_PORT]`
*   **Functionality:**
    *   Drops the existing database.
    *   Creates a new database.
    *   Restores the data from the specified backup file.
*   **Prerequisites:**
    *   The `.env` file must contain the `DB_NAME`, `POSTGRES_ADMIN_USER`, and `POSTGRES_ADMIN_PASSWORD` variables.
*   **Warning:** This is a destructive operation that will completely erase the existing database.

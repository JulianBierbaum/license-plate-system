# Development Environment Setup

This guide provides detailed instructions for setting up a local development environment for the License Plate Recognition System.

## 1. Prerequisites

Ensure you have installed all the necessary tools as described in the [Prerequisites](../getting-started/prerequisites.md) section.

## 2. Cloning the Repository

Clone the project repository from GitHub:

```bash
git clone <repository-url>
cd license-plate-system
```

## 3. Configuring the Environment

Create a `.env` file in the project root. This file will hold all your local configuration. You can refer to the [Configuration](../getting-started/configuration.md) guide for a complete list of environment variables.

For a basic local setup, you will need to define the following variables:

```env
# PostgreSQL
DB_HOST=postgres
DB_PORT=5432
DB_PORT_EXTERNAL=5432
DB_NAME=license-plate-system
POSTGRES_ADMIN_USER=admin
POSTGRES_ADMIN_PASSWORD=admin

# Schemas
DATA_COLLECTION_SCHEMA=data_collection
ANALYTICS_SCHEMA=analytics
NOTIFICATION_SCHEMA=notification

# Service Users
ANALYTICS_DB_USER=analytics
ANALYTICS_DB_PASSWORD=analytics
DATA_COLLECTION_DB_USER=data_collection
DATA_COLLECTION_DB_PASSWORD=data_collection
NOTIFICATION_DB_USER=notification
NOTIFICATION_DB_PASSWORD=notification

# Plate Recognizer
LICENSE_KEY=
PLATE_RECOGNIZER_API_KEY=

# Synology
SYNOLOGY_HOST=
SYNOLOGY_USERNAME=
SYNOLOGY_PASSWORD=

# Other
SAVE_DIR=./snapshots
INTERVAL_SECONDS=60
PLATE_RECOGNIZER_SERVICE_URL=http://plate-recognizer:8080/v1/plate-reader/
ACTIVE_DIRECTORY_URL=
ANALYTICS_SERVICE_URL=http://analytics-service:5000
NOTIFICATION_SERVICE_URL=http://notification-service:5000
AUTH_SERVICE_URL=http://auth-service:5000
SENDER_ADDRESS=
```

## 4. Running the Application

Use the `run.sh` script to start the development stack:

```bash
./run.sh
```

This will start all the services with hot-reloading enabled for the source code. Any changes you make to the code in the `services` directory will automatically trigger a restart of the corresponding service.

## 5. Database Migrations

The project uses Alembic for database migrations. When you make changes to the database models, you will need to create a new migration script.

To create a new migration script, run the following command:

```bash
docker compose run --rm db-prestart alembic revision --autogenerate -m "Your migration message"
```

This will generate a new migration script in the `db/alembic/versions` directory. The migrations are automatically applied when the `db-prestart` service starts.

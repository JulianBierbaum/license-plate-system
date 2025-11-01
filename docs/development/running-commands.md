# Running Commands

This section explains how to run various development commands, such as running tests and managing database migrations.

## Running Tests with Pytest

Each Python service in this project is equipped with a set of tests that can be run using `pytest`. To run the tests for a specific service, you can use the `docker-compose run` command.

For example, to run the tests for the `data-collection-service`:

```bash
docker-compose -f docker-compose.dev.yaml run --rm data-collection-service pytest
```

This command starts a new container for the `data-collection-service`, runs `pytest`, and then removes the container.

You can run tests for other services by replacing `data-collection-service` with the name of the service you want to test (e.g., `notification-service`, `analytics-service`).

## Managing Database Migrations with Alembic

The project uses Alembic to manage database schema migrations. The migration scripts are located in the `db/alembic/versions` directory.

### Creating a New Migration

When you make changes to the database models (e.g., in `services/data-collection-service/src/models/vehicle_observation.py`), you need to generate a new migration script.

To do this, run the following command:

```bash
docker-compose -f docker-compose.dev.yaml run --rm db-prestart alembic revision --autogenerate -m "A descriptive message about your changes"
```

This will create a new migration file in the `db/alembic/versions` directory.

### Applying Migrations

The database migrations are automatically applied when the `db-prestart` service starts. This service runs before any of the other services that depend on the database, ensuring that the schema is up-to-date.

If you need to manually apply migrations, you can run:

```bash
docker-compose -f docker-compose.dev.yaml run --rm db-prestart alembic upgrade head
```

### Downgrading Migrations

To downgrade a migration, you can use the `alembic downgrade` command. For example, to downgrade by one revision:

```bash
docker-compose -f docker-compose.dev.yaml run --rm db-prestart alembic downgrade -1
```

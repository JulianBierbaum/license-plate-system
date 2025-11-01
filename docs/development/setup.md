# Development Environment Setup

This guide provides detailed instructions for setting up a local development environment for the License Plate Recognition System.

## 1. Prerequisites

Ensure you have installed all the necessary tools as described in the [Getting Started Section](../getting-started/prerequisites.md).

## 2. Database Migrations

The project uses Alembic for database migrations. When you make changes to the database models, you will need to create a new migration script.

To create a new migration script, run the following command:

```bash
docker compose run --rm db-prestart alembic revision --autogenerate -m "Your migration message"
```

This will generate a new migration script in the `db/alembic/versions` directory. The migrations are automatically applied when the `db-prestart` service starts.

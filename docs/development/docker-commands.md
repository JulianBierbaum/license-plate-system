# Common Docker Commands

This section provides a reference for common Docker commands used in this project.

## Starting the Application

To start the application in development mode with hot-reloading, use the `run.sh` script:

```bash
./run.sh
```

This is the recommended way to start the application for development.

Alternatively, you can use `docker-compose` directly:

```bash
docker-compose -f docker-compose.dev.yaml up --build
```

To start the application in production mode, use the `docker-compose.prod.yaml` file:

```bash
docker-compose -f docker-compose.prod.yaml up -d --build
```

## Stopping the Application

To stop the application, you can use `Ctrl+C` in the terminal where the application is running if you did not use the `-d` flag.

If you used the `-d` flag to run the application in detached mode, you can stop it with:

```bash
docker-compose -f docker-compose.dev.yaml down
```

or for production:

```bash
docker-compose -f docker-compose.prod.yaml down
```

The `run.sh` script has a cleanup function that automatically runs `docker compose down` on exit.

## Viewing Logs

To view the logs of all running services, you can use the following command:

```bash
docker-compose -f docker-compose.dev.yaml logs -f
```

To view the logs of a specific service, you can specify the service name:

```bash
docker-compose -f docker-compose.dev.yaml logs -f <service-name>
```

For example, to view the logs of the `data-collection-service`:

```bash
docker-compose -f docker-compose.dev.yaml logs -f data-collection-service
```

## Executing Commands in Services

You can execute commands inside a running service container using `docker-compose exec`.

For example, to open a shell in the `data-collection-service` container:

```bash
docker-compose -f docker-compose.dev.yaml exec data-collection-service bash
```

This is useful for debugging and running commands within the context of a specific service.

## Running One-off Commands

To run a one-off command in a service container, you can use `docker-compose run`. This is particularly useful for tasks like running tests or database migrations.

For example, to run `pytest` in the `data-collection-service`:

```bash
docker-compose -f docker-compose.dev.yaml run --rm data-collection-service pytest
```

The `--rm` flag automatically removes the container after the command exits.

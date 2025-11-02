# Troubleshooting

This section lists common issues you might encounter during development and how to resolve them.

## Services are not starting

If the services are not starting correctly, here are a few things to check:

*   **`.env` file:** Ensure that your `.env` file is correctly configured and that all necessary environment variables are set.
*   **Docker is running:** Make sure that the Docker daemon is running.
*   **Ports are available:** Check if the ports used by the services are not already in use by other applications. You can see the ports in the `docker-compose.dev.yaml` file.
*   **Docker Compose logs:** Check the logs for any error messages:
    ```bash
    docker compose -f docker-compose.dev.yaml logs -f
    ```

## `db-prestart` service fails

If the `db-prestart` service fails, it is likely due to an issue with the database migrations.

*   **Check the logs:** Look at the logs of the `db-prestart` service for any error messages from Alembic.
*   **Migration conflicts:** If you have been working on a feature branch and have a conflict with migrations from the `main` branch, you may need to resolve the conflict manually. You can do this by editing the migration files in `db/alembic/versions`.

## Permission errors with backup directory

You might need to give write-access to the backup-location folder to all user groups.

If you are getting permission errors when running the backup scripts, you can try changing the permissions of the backup directory:

```bash
sudo chmod -R 777 /path/to/your/backup/directory
```

## `build.sh` script fails

If the `build.sh` script fails, here are a few things to check:

*   **`DOCKER_REGISTRY` environment variable:** Make sure that the `DOCKER_REGISTRY` environment variable is set in your `.env` file.
*   **Lock files:** The `build.sh` script checks for `uv.lock` and `package-lock.json` files. If these files are missing, you will need to generate them by running `uv lock` or `npm install` in the respective service directories.
*   **Docker Hub login:** If you are pushing to a private Docker Hub repository, you will need to be logged in to Docker Hub. You can log in with the `docker login` command.

# Docker Compose Reference

This project uses Docker Compose to manage the multi-container application stack. There are two main Docker Compose files: `docker-compose.dev.yaml` for development and `docker-compose.prod.yaml` for production.

## `docker-compose.dev.yaml`

This file is used for local development.

*   **Builds services locally:** It builds the Docker images for the services from the local source code.
*   **Hot-reloading:** It mounts the source code directories as volumes, which enables hot-reloading when you make changes to the code.
*   **Debug-friendly:** It sets the `LOG_LEVEL` to `DEBUG` by default, providing more verbose logging for development.
*   **Exposes ports:** It exposes the ports of the services to the host machine, so you can access them directly.

## `docker-compose.prod.yaml`

This file is intended for production deployments.

*   **Uses pre-built images:** It pulls the service images from a Docker registry, rather than building them locally.
*   **No volume mounts for source code:** The source code is not mounted as volumes, as the images are expected to be self-contained.
*   **Restart policy:** It includes a `restart: unless-stopped` policy for the services, so that they are automatically restarted if they crash.
*   **Optimized for production:** It is configured for production use, with less verbose logging and no development-specific features.

## Key Differences

| Feature             | `docker-compose.dev.yaml`      | `docker-compose.prod.yaml`     |
| ------------------- | ------------------------------ | ------------------------------ |
| **Image Source**    | Builds from local source       | Pulls from Docker registry     |
| **Source Code**     | Mounted as volumes             | Not mounted                    |
| **Hot-reloading**   | Enabled                        | Disabled                       |
| **`LOG_LEVEL`**     | `DEBUG` (default)              | Set via `.env` file            |
| **Restart Policy**  | Not set                        | `unless-stopped`               |

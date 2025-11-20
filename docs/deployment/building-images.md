# Building and Pushing Docker Images

This section describes how to build the Docker images for the services and push them to a Docker registry.

## Automated Builds with GitHub Actions

The project is configured to automatically build and push Docker images to a Docker registry whenever code is pushed to the `main` branch. This process is managed by the GitHub Actions workflow defined in `.github/workflows/docker-build.yaml`.

The workflow uses the `build.sh` script to build and push the images.

### Secrets

The GitHub Actions workflow requires the following secrets to be configured in the repository settings:

*   `DOCKER_REGISTRY`: The URL of the Docker registry.
*   `DOCKER_USERNAME`: The username for the Docker registry.
*   `DOCKER_TOKEN`: A personal access token with permissions to push images to the registry.

## Manual Builds

You can also build and push the images manually using the `build.sh` script.

### Usage

```bash
./build.sh
```

### Prerequisites

Before running the script, you need to:

1.  **Set the `DOCKER_REGISTRY` environment variable:** This variable must be set in your `.env` file. It should point to the Docker registry where you want to push the images.
2.  **Log in to the Docker registry:** You need to be authenticated with the Docker registry. You can do this using the `docker login` command:
    ```bash
    docker login <your-docker-registry>
    ```
3.  **Ensure lock files are present:** The script checks for the existence of `uv.lock` (for Python services) and `package-lock.json` (for the web service). If these files are missing, you need to generate them by running `uv lock` or `npm install` in the respective service directories.

### Script Details

The `build.sh` script iterates through all the services in the `services` directory, builds a Docker image for each service, and then pushes the image to the configured Docker registry. It also builds and pushes images for `db-prestart`, `db-backup`, `shared-data`, and `grafana`.

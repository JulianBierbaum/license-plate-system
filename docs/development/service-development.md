# Service Development

This guide outlines the process for developing, adding, and extending Python services in the License Plate Recognition System.

## Dependency Management

Each service uses `uv` for dependency management. When working on a service, ensure you use `uv` to manage packages and virtual environments.

## Dockerfile

New services should use the standard `uv` Dockerfile pattern found in existing services. This ensures consistency and proper caching.

## Docker Compose

When adding a new service, it must be added to **BOTH** `docker-compose.dev.yaml` and `docker-compose.prod.yaml`.

*   **Development (`docker-compose.dev.yaml`)**: Use the `build` context and mount volumes (e.g., `./services/<service>/src:/app/src`) to enable hot-reloading during development.
*   **Production (`docker-compose.prod.yaml`)**: Use the built image (e.g., `image: julianbierbaum/license-plate-system:<service>`) and appropriate restart policies (`restart: on-failure`).

## Environment Variables

If your service requires environment variables:

1.  Add them to your local `.env` file.
2.  Add them to `.env.example` so other developers know they are required. But make sure to censor all sensitive variables in this file because its publicly viewable.

## Build Script

You should *NOT* edit the `build.sh` script if you dont explicitly need to. 

The `build.sh` script automatically iterates through directories in `services/`. It will build and push your service if it detects the following files:
*   `Dockerfile`
*   `pyproject.toml`
*   `uv.lock`

## CI/CD Workflows

When adding a new service, you **MUST** update the GitHub Actions workflow at `.github/workflows/ci-cd.yaml`.
Add steps for:
*   **Linting**: Run `ruff check` and `ruff format` on your service.
*   **Testing**: Run `pytest` for your service.

Failure to do this will result in your service not being tested in the CI pipeline.

## Documentation

When adding or modifying a service, remember to update the relevant documentation:

*   **Configuration**: Update `docs/getting-started/configuration.md` if you added new environment variables.
*   **API Reference**: Update `docs/reference/api.md` if your service exposes new API endpoints.

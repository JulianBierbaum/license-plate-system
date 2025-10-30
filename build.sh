#!/bin/bash

# Build and push all project services
# Usage: ./build.sh

set -e

# Load environment variables from .env file
if [ -f ".env" ]; then
    set -a
    source ".env"
    set +a
else
    echo "Error: .env file not found in project root"
    exit 1
fi

DOCKER_REGISTRY="${DOCKER_REGISTRY}"

# Check for required lock files before building
if [ -f "db/pyproject.toml" ] && [ ! -f "db/uv.lock" ]; then
  echo "Error: db/uv.lock not found. Run 'cd db && uv lock' first."
  exit 1
fi

# Build db-prestart
echo "--- Building db-prestart ---"
docker build -t "${DOCKER_REGISTRY}:db-prestart" -f ./db/Dockerfile .
docker push "${DOCKER_REGISTRY}:db-prestart"

# Build db-backup
echo "--- Building db-backup ---"
docker build -t "${DOCKER_REGISTRY}:db-backup" -f ./db-backup/Dockerfile ./db-backup
docker push "${DOCKER_REGISTRY}:db-backup"

# Build shared-data
echo "--- Building shared-data ---"
docker build -f shared-data/Dockerfile -t "${DOCKER_REGISTRY}:shared-data" ./shared-data
docker push "${DOCKER_REGISTRY}:shared-data"

# Build all services
for SERVICE_DIR in services/*/; do
  SERVICE_NAME=$(basename "$SERVICE_DIR")
  echo "--- Building ${SERVICE_NAME} ---"

  # Check Python lock file
  if [ -f "${SERVICE_DIR}pyproject.toml" ] && [ ! -f "${SERVICE_DIR}uv.lock" ]; then
    echo "Error: ${SERVICE_DIR}uv.lock not found. Run uv sync first."
    exit 1
  fi

  # Check Node.js lock file
  if [ -f "${SERVICE_DIR}package.json" ] && [ ! -f "${SERVICE_DIR}package-lock.json" ]; then
    echo "Error: ${SERVICE_DIR}package-lock.json not found. Run npm install first."
    exit 1
  fi

  docker build -t "${DOCKER_REGISTRY}:${SERVICE_NAME}" "$SERVICE_DIR"
  docker push "${DOCKER_REGISTRY}:${SERVICE_NAME}"
done

echo "Build and push completed successfully!"

#!/bin/bash

# Build script for the project services
# Usage: ./build.sh [-p for pushing to docker registry] [list of service names seperated by spaces]

set -e

REPO="julianbierbaum/license-plate-system"
PUSH=false
SERVICES_TO_BUILD=()


while [[ $# -gt 0 ]]; do
  case "$1" in
    -p)
      PUSH=true
      shift
      ;;
    *)
      SERVICES_TO_BUILD+=("$1")
      shift
      ;;
  esac
done

if [ ${#SERVICES_TO_BUILD[@]} -eq 0 ]; then
  SERVICES_TO_BUILD=($(basename -a services/*/))
fi

# Check for required lock files before building
if [ -f "db/pyproject.toml" ] && [ ! -f "db/uv.lock" ]; then
  echo "Error: db/uv.lock not found. Run 'cd db && uv lock' first."
  exit 1
fi

# Build db-prestart
docker build -t "${REPO}:db-prestart" -f ./db/Dockerfile .
if [ "$PUSH" = true ]; then
  docker push "${REPO}:db-prestart"
fi

# Build db-backup
docker build -t "${REPO}:db-backup" -f ./db-backup/Dockerfile ./db-backup
if [ "$PUSH" = true ]; then
  docker push "${REPO}:db-backup"
fi

# Build shared-data
docker build -f shared-data/Dockerfile -t "${REPO}:shared-data" ./shared-data
if [ "$PUSH" = true ]; then
  docker push "${REPO}:shared-data"
fi

# Build services
for SERVICE_NAME in "${SERVICES_TO_BUILD[@]}"; do
  SERVICE_DIR="services/${SERVICE_NAME}/"

  if [ ! -d "$SERVICE_DIR" ]; then
    echo "Service '$SERVICE_NAME' not found in services/"
    exit 1
  fi

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

  docker build -t "${REPO}:${SERVICE_NAME}" "$SERVICE_DIR"

  if [ "$PUSH" = true ]; then
    docker push "${REPO}:${SERVICE_NAME}"
  fi
done

echo "Build completed successfully!"

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

(cd db && uv sync)
docker build -t "${REPO}:db-prestart" -f ./db/Dockerfile .
if [ "$PUSH" = true ]; then
  docker push "${REPO}:db-prestart"
fi

docker build -f shared-data/Dockerfile -t "${REPO}:shared-data" ./shared-data
if [ "$PUSH" = true ]; then
  docker push "${REPO}:shared-data"
fi

for SERVICE_NAME in "${SERVICES_TO_BUILD[@]}"; do
  SERVICE_DIR="services/${SERVICE_NAME}/"
  if [ ! -d "$SERVICE_DIR" ]; then
    echo "Service '$SERVICE_NAME' not found in services/"
    exit 1
  fi

  if [ -f "${SERVICE_DIR}pyproject.toml" ]; then
    (cd "$SERVICE_DIR" && uv sync)
  fi

  if [ -f "${SERVICE_DIR}package.json" ]; then
    (cd "$SERVICE_DIR" && npm install)
  fi

  docker build -t "${REPO}:${SERVICE_NAME}" "$SERVICE_DIR"

  if [ "$PUSH" = true ]; then
    docker push "${REPO}:${SERVICE_NAME}"
  fi
done

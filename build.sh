#!/bin/bash
set -e

REPO="julianbierbaum/license-plate-system"
PUSH=false

while getopts ":p" opt; do
  case ${opt} in
    p )
      PUSH=true
      ;;
    \? )
      echo "Invalid option: -$OPTARG" 1>&2
      exit 1
      ;;
  esac
done

(cd db && uv sync)
docker build -t "${REPO}:db-migrator" -f ./db/Dockerfile .
if [ "$PUSH" = true ]; then
  docker push "${REPO}:db-migrator"
fi

for SERVICE_DIR in services/*/; do
  SERVICE_NAME=$(basename "$SERVICE_DIR")
  if [ -f "${SERVICE_DIR}pyproject.toml" ]; then
    (cd "$SERVICE_DIR" && uv sync)
  fi

  if [ -f "${SERVICE_DIR}package.json" ]; then
    (cd "$SERVICE_DIR" && npm install)
  fi

  docker build -t "${REPO}:${SERVICE_NAME}" ./"$SERVICE_DIR"

  if [ "$PUSH" = true ]; then
    docker push "${REPO}:${SERVICE_NAME}"
  fi
done

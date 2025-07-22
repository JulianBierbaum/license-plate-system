#!/bin/bash

# Function to be executed on exit
cleanup() {
    echo "Stopping services and removing volumes..."
    docker-compose down -v
}

# Trap the EXIT signal and execute the cleanup function
trap cleanup EXIT

# Start the services
docker-compose up

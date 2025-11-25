# Production Deployment Guide

This guide outlines the steps for deploying the License Plate Recognition System in a production environment.

## 1. Prerequisites

*   A server or cluster with Docker and Docker Compose installed.
*   A Docker registry containing the images for all the services. See the [Building and Pushing Docker Images](building-images.md) guide for more information.
*   A PostgreSQL database. You can run the database in a Docker container, as shown in the `docker-compose.prod.yaml` file, or use a managed database service.

## 2. Configuration

Create a `.env` file on the production server with the appropriate environment variables for your production environment. You can refer to the [Configuration](../getting-started/configuration.md) guide for a complete list of variables.

**Important:** Do not use the default development passwords...

## 3. Docker Compose for Production

The `docker-compose.prod.yaml` file is provided as a starting point for production deployments. This file is similar to the `dev` version, but it uses the images from the Docker registry instead of building them locally, and it does not mount the source code volumes.

You can use this file directly or adapt it to your needs. If for example you wanted to use k8s.

## 4. Deployment Steps

1.  **Copy `docker-compose.prod.yaml` to the server:** Transfer the `docker-compose.prod.yaml` file to your production server.
2.  **Create the `.env` file:** Create a `.env` file on the server with your production configuration.
3.  **Log in to the Docker registry:** If your Docker registry requires authentication (the default one does not), log in using the `docker login` command.
4.  **Start the application:** Use Docker Compose to start the application in detached mode:

    ```bash
    docker compose -f docker-compose.prod.yaml up -d
    ```

This will pull the required images from your Docker registry and start all the services.
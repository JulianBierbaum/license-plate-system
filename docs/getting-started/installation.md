# Installation

Follow these steps to get the License Plate Recognition System up and running on your local machine for development and testing purposes.

## 1. Clone the Repository

First, clone the project repository from GitHub to your local machine:

```bash
git clone <repository-url>
cd license-plate-system
```

## 2. Configure Environment Variables

The system uses a `.env` file to manage environment variables. You will need to create a `.env` file in the root of the project and populate it with the necessary configuration.

A good starting point is to copy the `.env.example` file if one exists, or to create a new file and add the variables as described in the [Configuration](configuration.md) section.

## 3. Start the Application

Once the environment variables are configured, you can start the application stack using Docker Compose. For development, you can use the `docker-compose.dev.yaml` file.

The easiest way to start the system is to use the provided `run.sh` script:

```bash
./run.sh
```

This script will build the necessary Docker images and start all the services defined in the `docker-compose.dev.yaml` file.

Alternatively, you can use `docker-compose` directly:

```bash
docker-compose -f docker-compose.dev.yaml up --build
```

## 4. Accessing the Services

Once the application is running, you can access the different services at their respective ports, as defined in the `docker-compose.dev.yaml` file.

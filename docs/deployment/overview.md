# Architecture Overview

The License Plate Recognition System is a microservices-based application, designed for containerized deployment. The entire system is orchestrated using Docker Compose.

## Services

The system is composed of the following services:

*   **`analytics-service`**: Provides analytics and insights on the collected license plate data.
*   **`auth-service`**: Handles user authentication and authorization, integrating with Active Directory.
*   **`data-collection-service`**: Polls the Synology NAS for new images, sends them to the Plate Recognizer service, and stores the results in the database.
*   **`notification-service`**: Sends notifications (e.g., email) based on predefined rules and events.
*   **`web-service`**: The frontend application, built with Next.js, that provides the user interface for the system.
*   **`plate-recognizer`**: A third-party service that performs the actual license plate recognition.
*   **`postgres`**: The PostgreSQL database that stores all the application data.
*   **`db-prestart`**: A service that runs database migrations before the other services start.
*   **`postgres-backup`**: A service that performs periodic backups of the database.

## Data Flow

1.  The **`data-collection-service`** periodically fetches images from a Synology NAS.
2.  These images are sent to the **`plate-recognizer`** service, which detects and reads license plates.
3.  The results from the `plate-recognizer` service are then stored in the **`postgres`** database by the `data-collection-service`.
4.  The **`web-service`** provides a user interface to view the collected data, and it communicates with the other backend services (`analytics-service`, `notification-service`, `auth-service`) to provide various features.
5.  The **`notification-service`** can be configured to send alerts based on the data collected.
6.  The **`analytics-service`** provides data for dashboards and reports in the `web-service`.

## Containerization

All services are containerized using Docker. This allows for a consistent and reproducible deployment across different environments. The `docker-compose.*.yaml` files define the services, their dependencies, and their configurations.

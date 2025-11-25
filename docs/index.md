# License Plate Recognition System Documentation

This documentation provides a comprehensive overview of the License Plate Recognition System, developed for Zotter Schokoladen GmbH.

---

## System Architecture

![System Architecture](assets/architecture-light.png#only-light)
![System Architecture](assets/architecture-dark.png#only-dark)

The system is designed as a modular, containerized application stack.  

---

## Quick Start

1.  **Set up Environment:** Copy the `.env.example` file to `.env` and ensure all environment variables are correctly set.
2.  **Start the System:** Use the `docker-compose.dev.yaml` file or the `./run.sh` script to start the application stack.

    ```bash
    ./run.sh
    ```

## Development

For detailed information on setting up a development environment, running tests, and contributing to the project, please see the **Development** section.

!!! note "Operating System Recommendation"
    This system is developed for a **Linux** environment. It is strongly recommended to develop on a **Unix-based system** (Linux or macOS). Windows users may encounter issues with line endings (CRLF vs LF) in scripts and configuration files, which can prevent the system from executing correctly.


## Operations

The **Operations** section provides guidance on essential maintenance tasks, including:

*   **Backups:** Performing manual and automatic database backups.
*   **Restore:** Restoring the database from a backup.

## Deployment

The system is designed for containerized deployment. Refer to the **Deployment** section for instructions on building and deploying the application in a production environment.

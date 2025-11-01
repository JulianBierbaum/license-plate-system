# Prerequisites

Before you begin, ensure you have the following tools installed on your system:

*   **Docker:** The application is fully containerized, so Docker is essential for running the services. You can download and install Docker from the official website.
*   **Docker Compose:** Docker Compose is used to manage the multi-container application stack. It is included with Docker Desktop for Windows and macOS. For Linux, you may need to install it separately.
*   **Git:** The project is managed with Git. You will need Git to clone the repository and manage versions.
*   **Shell Environment:** A shell environment like Bash is required to run the provided scripts (`.sh` files).
*   **Text Editor/IDE:** You will need a text editor or Integrated Development Environment (IDE) to edit configuration files.

## Hardware Requirements

In addition to the software prerequisites, the following hardware is required for the system to function correctly:

*   **Synology NAS:** A Synology Network Attached Storage (NAS) device is required to store the images from the cameras. The `data-collection-service` is specifically designed to poll a Synology NAS.
*   **IP Cameras:** IP cameras are needed to capture the images of the license plates. These cameras should be configured to save the images to the Synology NAS.
*   **Server:** A server to host the application stack. The server should have enough resources (CPU, RAM, disk space) to run all the Docker containers (or just use the NAS).
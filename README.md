# // License Plate System
License plate recognition system for Zotter Schokoladen GmbH.

### / Dev Environment Setup
1. Make sure all environment variables are set correctly in the .env file.
<br>
2. Run the `build.sh` script to build images.
    - Usage: `./build.sh [-p] [SERVICE...]`
    - Optional Arguments
        - `-p` Push the built images to the Docker registry
        - `SERVICE...` One or more service names to build, separated by spaces
<br>
3. Now you can start the docker stack manually or use the `./run` script.

<br>

**Development Commands:**
If you need to run a command for development purposes e.g. pytest or alambic revision it is recommended to do so inside of a running instance of that service.

Example:
`docker compose run --rm db-prestart alembic revision --autogenerate -m "name_of_revision"`

<br>

**Notes:**
- You might need to give write-access to the backup-location folder to all user groups.
- Make script files executable if neccesary.

---

### / Backups & Restore
The `postgres-backup` service creates periodic backups based on the schedule in cron format defined in the `BACKUP_SCHEDULE` environment variable. If the variable is empty or not set no periodic backups are performed.
The retention time of the automatic backups can be defined via the `BACKUP_RETENTION_DAYS` variable.
<br>
Manual backups can be performed using the `manual_backup.sh` script.
The Backups will be saved to the backup directory defined in the environment variables.
- Usage: `./backup.sh <BACKUP_NAME>`
<br>

Both manual and automatic backups can be restored to the database using the `restore_backup.sh` script.
Note that this requires the services to be stopped for the duration of the restoration process.
- Usage: `./restore.sh <PATH_TO_BACKUP_FILE>`
---

### / Deployment
The project uses a fully containerized architecture, allowing straightforward deployment.
All service images are production-ready and can be deployed without modifying the service code.

Steps:
1. Build images and push them to a docker registry if deployment is on a different machine.
2. Define Service Dependencies. You can use the provided `docker-compose.yaml` file and modify it for production needs or use a different container orchestrator (e.g. k8s).
3. Ensure the required env variables are set in the production environment
4. Deploy System
# license-plate-system
License plate recognition system for Zotter Schokoladen GmbH

### Setup
- run the `build.sh` file to build images. You can specify services to build by adding their name seperated by space and add the `-p` flag to push them to docker registry.
- run `docker compose up` to start the development stack

**Add new Alembic Revision:**
- `docker compose run --rm db-prestart alembic revision --autogenerate -m "text"`
# license-plate-system
License plate recognition system for Zotter Schokoladen GmbH

### Setup
- run the `build.sh` file to build images and add the `-p` flag to push them to docker registry. IMPORTANT: always build all images together
- run `docker compose up` to start the development stack

**Add new Alembic Revision:**
- `docker compose run --rm db-migrator alembic revision --autogenerate -m "text"`
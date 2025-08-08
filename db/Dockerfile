FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

# Install the project into `/app`
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Install the project's dependencies using the lockfile and settings
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=/db/uv.lock,target=uv.lock \
    --mount=type=bind,source=/db/pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

# Then, add the rest of the project source code and install it
COPY /db /app

COPY services/data-collection-service/src/ /app/data_collection/src/
COPY services/notification-service/src/ /app/notification/src/
# COPY services/analytics-service/src/ /app/analytics/src/

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app/"

RUN chmod +x entrypoint.sh

# Reset the entrypoint, don't invoke `uv`
ENTRYPOINT []

# Start shell script
CMD ["./entrypoint.sh"]
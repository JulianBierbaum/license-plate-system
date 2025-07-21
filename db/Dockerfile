FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

# Install PostgreSQL client for psql usage
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install project dependencies into that virtualenv
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    uv sync --locked --no-dev

# Copy app source code
COPY . /app

# Make entrypoint executable
RUN chmod +x entrypoint.sh

# Step 6: Use .venv in PATH
ENV PATH="/app/.venv/bin:$PATH"

ENTRYPOINT []
CMD ["./entrypoint.sh"]

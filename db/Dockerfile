FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

# Install PostgreSQL client for psql usage
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-dev

ENV PATH="/app/.venv/bin:$PATH"


COPY . /app


RUN chmod +x entrypoint.sh

ENTRYPOINT []

CMD ["./entrypoint.sh"]
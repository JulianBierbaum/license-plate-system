import os
import sys
from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context
from alembic.config import Config

# Add the /app directory to the Python path
sys.path.insert(0, '/app')

# Import Base objecz
from data_collection.src.models.base import IngestionBase
from notification.src.models.base import NotificationBase
# from analytics.src.models.base import AnalyticsBase

config: Config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = [
    IngestionBase.metadata,
    NotificationBase.metadata,
    # AnalyticsBase.metadata,
]


def run_migrations_offline() -> None:
    url = config.get_main_option('sqlalchemy.url')
    context.configure(
        url=url,
        target_metadata=target_metadata,
        include_schemas=True,
        literal_binds=True,
        dialect_opts={'paramstyle': 'named'},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    db_host = os.getenv('DB_HOST')
    db_port = os.getenv('DB_PORT')
    db_name = os.getenv('DB_NAME')

    sqlalchemy_url = f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'

    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        url=sqlalchemy_url,
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            include_schemas=True,
            compare_type=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

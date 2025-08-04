import os

from pydantic import PostgresDsn
from pydantic_core import MultiHostUrl


class Settings:
    """settings class"""

    db_user: str = os.getenv("DB_USER", "")
    db_password: str = os.getenv("DB_PASSWORD", "")
    db_host: str = os.getenv("DB_HOST", "")
    db_port: str = os.getenv("DB_PORT", "")
    db_name: str = os.getenv("DB_NAME", "")
    notification_schema: str = os.getenv("NOTIFICATION_SCHEMA", "")
    log_level: str = os.getenv("LOG_LEVEL", "").upper()
    analytics_service_url: str = os.getenv("ANALYTICS_SERVICE_URL", "")
    sender_address: str = os.getenv("SENDER_ADDRESS", "")
    app_password: str = os.getenv("APP_PASSWORD", "")

    @property
    def db_uri(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+psycopg2",
            username=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=int(self.db_port),
            path=self.db_name,
        )


settings = Settings()

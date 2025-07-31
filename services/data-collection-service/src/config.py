import os

from pydantic import PostgresDsn
from pydantic_core import MultiHostUrl


class Settings:
    """settings class
    """
    db_user: str = os.getenv("DB_USER", "")
    db_password: str = os.getenv("DB_PASSWORD", "")
    db_host: str = os.getenv("DB_HOST", "")
    db_port: str = os.getenv("DB_PORT", "")
    db_name: str = os.getenv("DB_NAME", "")
    log_level: str = os.getenv("LOG_LEVEL", "").upper()
    synology_host: str = os.getenv("SYNOLOGY_HOST", "")
    synology_username: str = os.getenv("SYNOLOGY_USERNAME", "")
    synology_password: str = os.getenv("SYNOLOGY_PASSWORD", "")
    api_key: str = os.getenv("API_KEY", "")

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

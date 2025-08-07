from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings for the Data Collection Service"""

    # Database settings
    db_user: str = Field(..., env="DB_USER")
    db_password: str = Field(..., env="DB_PASSWORD")
    db_host: str = Field(..., env="DB_HOST")
    db_port: int = Field(..., env="DB_PORT")
    db_name: str = Field(..., env="DB_NAME")
    data_collection_schema: str = Field(..., env="DATA_COLLECTION_SCHEMA")

    # Service-specific settings
    log_level: str = Field("INFO", env="LOG_LEVEL")
    synology_host: str = Field(..., env="SYNOLOGY_HOST")
    synology_username: str = Field(..., env="SYNOLOGY_USERNAME")
    synology_password: str = Field(..., env="SYNOLOGY_PASSWORD")
    api_key: str = Field(..., env="API_KEY")
    save_images_for_debug: str = Field(..., env="SAVE_IMAGES_FOR_DEBUG")

    @property
    def db_uri(self) -> PostgresDsn:
        """Constructs the PostgreSQL connection URI."""
        return PostgresDsn.build(
            scheme="postgresql+psycopg2",
            username=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            path=self.db_name,
        )


settings = Settings()

from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings for the Data Collection Service"""

    # Database settings
    db_user: str = Field(..., alias='DB_USER')
    db_password: str = Field(..., alias='DB_PASSWORD')
    db_host: str = Field(..., alias='DB_HOST')
    db_port: int = Field(..., alias='DB_PORT')
    db_name: str = Field(..., alias='DB_NAME')
    data_collection_schema: str = Field(..., alias='DATA_COLLECTION_SCHEMA')

    # Service-specific settings
    log_level: str = Field('INFO', alias='LOG_LEVEL')
    synology_host: str = Field(..., alias='SYNOLOGY_HOST')
    synology_username: str = Field(..., alias='SYNOLOGY_USERNAME')
    synology_password: str = Field(..., alias='SYNOLOGY_PASSWORD')
    api_key: str = Field(..., alias='API_KEY')
    save_images_for_debug: bool = Field(False, alias='SAVE_IMAGES_FOR_DEBUG')
    interval_seconds: int = Field(60, alias='INTERVAL_SECONDS')
    plate_recognizer_service_url: str = Field(..., alias="PLATE_RECOGNIZER_SERVICE_URL")

    @property
    def db_uri(self) -> PostgresDsn:
        """Constructs the PostgreSQL connection URI."""
        return PostgresDsn.build(
            scheme='postgresql+psycopg2',
            username=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            path=self.db_name,
        )


settings = Settings()

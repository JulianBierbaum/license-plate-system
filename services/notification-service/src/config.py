from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings for the Notification Service"""

    # Database settings
    db_user: str = Field(..., alias='DB_USER')
    db_password: str = Field(..., alias='DB_PASSWORD')
    db_host: str = Field(..., alias='DB_HOST')
    db_port: int = Field(..., alias='DB_PORT')
    db_name: str = Field(..., alias='DB_NAME')
    notification_schema: str = Field(..., alias='NOTIFICATION_SCHEMA')

    # Service-specific settings
    log_level: str = Field('INFO', alias='LOG_LEVEL')
    analytics_service_url: str = Field(..., alias='ANALYTICS_SERVICE_URL')
    sender_address: str = Field(..., alias='SENDER_ADDRESS')

    # SMTP settings
    smtp_relay_host: str = Field(..., alias='SMTP_RELAY_ADDRESS')
    smtp_port: int = Field(25, alias='SMTP_PORT')

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

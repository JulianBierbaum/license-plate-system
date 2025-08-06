from pydantic_settings import BaseSettings
from pydantic import computed_field
import os
from src.exceptions.exceptions import NotFoundException


class Settings(BaseSettings):
    API_V1_STR: str = "/auth/v1"
    PROJECT_NAME: str = "Authentication_Service"

    # Logging
    LOG_LEVEL: str = "INFO"

    # JWT
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EPIRE_MINUTES: int = 1
    SECRET_KEY: str

    # Active Directory
    DOMAIN_NAME: str
    DOMAIN_LOCAL: str
    AD_USERNAME: str
    PASSWORD: str
    SERVER_IP: str

    class Config:
        env_file = ".env"   # <-- THIS loads your .env automatically
        env_file_encoding = "utf-8"

    # # service specific variables
    # API_V1_STR: str = "/auth/v1"
    # PROJECT_NAME: str = "Authentication_Service"
    # #logging
    # log_level: str = os.getenv("LOG_LEVEL", "").upper()

    # # JWT related variables
    # ALGORITHM: str = "HS256"
    # ACCESS_TOKEN_EPIRE_MINUTES: int = 1  # Minutes
    # SECRET_KEY: str = os.getenv("SECRET_KEY", "")

    # # AD related variables
    # DOMAIN_NAME: str = os.getenv("DOMAIN_NAME", "")
    # DOMAIN_LOCAL: str = os.getenv("DOMAIN_LOCAL", "")
    # AD_USERNAME: str = os.getenv("AD_USERNAME", "")
    # PASSWORD: str = os.getenv("PASSWORD", "")
    # SERVER_IP: str = os.getenv("PASSWORD", "")
    

    @computed_field
    def DN(self) -> str:
        return f"{self.DOMAIN_NAME}.{self.DOMAIN_LOCAL}"

    print(DN)
    @computed_field
    def ROOT_DN(self) -> str:
        return f"dc={self.DOMAIN_NAME},dc={self.DOMAIN_LOCAL}" # DN: Domain name, eg.: name.at


settings = Settings()


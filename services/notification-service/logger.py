import logging

from src.config import settings

logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s - notification-service - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger(__name__)

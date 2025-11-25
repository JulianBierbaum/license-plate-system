import logging

from src.config import settings

logging.basicConfig(
    level=settings.log_level,
    format='%(asctime)s - data-collection-service - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()],
)

logger = logging.getLogger(__name__)

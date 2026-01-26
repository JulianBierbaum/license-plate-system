from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

from src.config import settings

api_key_header = APIKeyHeader(name='Authorization', auto_error=True)


async def verify_api_key(api_key: str = Security(api_key_header)) -> str:
    """Verify the API key from request header.

    Args:
        api_key: API key from header

    Returns:
        The API key if valid

    Raises:
        HTTPException: 401 if API key is invalid
    """
    if api_key != settings.api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid API key',
        )
    return api_key

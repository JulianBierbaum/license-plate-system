from datetime import datetime, timezone, timedelta

import jwt
from src.core.config import settings
from src.core.ad_client import verify_login
from src.exceptions.exceptions import TokenExpiredException
from src.schemas.login import Token_Authenticate
from src.logger import logger


def authenticate_token(token):
    """verify the credibility of a token

    Args:
        token (string): Your JWT

    Returns:
        1: Token credible
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        exp = payload["exp"]
        if exp <= datetime.now(timezone.utc):
            raise TokenExpiredException
    except Exception:
        raise Exception
    return 1


def new_token(username: str, password: str) -> str:
    """create a new JWT using username and password

    Args:
        username (str): username of AD user (only username, no special domain formatting)
        password (str): plain text password of user username

    Returns:
        str: credible input, returns new token
    """
    logger.info(username)
    verify_login(username, password)
    payload = {
        "username": username,
        "exp": datetime.now(timezone.utc)
        + timedelta(minutes=settings.ACCESS_TOKEN_EPIRE_MINUTES),
    }
    token = jwt.encode(payload, settings.SECRET_KEY, settings.ALGORITHM)
    return token

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from src.exceptions.exceptions import TokenExpiredException

import src.schemas.login as schemas

from src.core.config import settings
import jwt
from datetime import datetime, timezone, timedelta


reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login"
)  # Extrahiert Token aus Bearer-Header; ist ein string

TokenDep = Annotated[str, Depends(reusable_oauth2)]


def _verify_token(token: TokenDep) -> schemas.Token_Data:  # dict[str, Any]:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
            options={"require": ["exp", "username"]}, 
        )
    except jwt.ExpiredSignatureError as exc:
        raise TokenExpiredException()
    except jwt.PyJWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Ungültiger oder manipulierter Token",
        ) from exc
    return schemas.Token_Data(
        username=payload["username"], exp=payload["exp"]
    )  


def get_current_user(token: TokenDep) -> schemas.User_Return:
    payload = _verify_token(token)
    return schemas.User_Return(username=payload.username) 


CurrentUser = Annotated[schemas.User_Return, Depends(get_current_user)]

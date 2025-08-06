from fastapi import APIRouter, Depends
from src.schemas import login as schemas
from src.core import security
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from src.api.deps import CurrentUser

router = APIRouter()


@router.post("/", response_model=schemas.Token_Response)
def create_jwt(
    user_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    """Validates your login-data and creates jwt if data is validated

    Args:
        user_data (Annotated[OAuth2PasswordRequestForm, Depends): login-data (username, password)

    Returns:
        schemas.Token_Response: the new jwt
    """
    return {
        "access_token": security.new_token(user_data.username, user_data.password),
        "token_type": "bearer",
    }


# @router.post("/check_token", response_model=)


@router.post("/me", response_model=schemas.User_Return)
def my_user_data(
    user_data: CurrentUser,
):  # CurrentUser aus deps = Annotated[schemas.User_Return, Depends(get_current_user)] also es muss get_current_user durchgehen
    return user_data

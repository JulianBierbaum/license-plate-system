from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute

from src.api.main import api_router
from src.core.config import settings

from src.exceptions.exceptions import (
    WrongInputException, MissingValueException, OperationFailedException, NotFoundException,
    DivisionByZeroException, TokenExpiredException, WrongLoginDataException
)
from src.exceptions.exception_handlers import (
    wrong_input_handler, missing_value_handler, operation_failed_handler, not_found_exception_handler,
    division_by_zero_handler, token_expired_handler
)

def cstm_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    generate_unique_id_function=cstm_generate_unique_id,
)

app.include_router(api_router, prefix=settings.API_V1_STR)

# @app.get("/")
# async def root():
#     return {"message": "Hello World!"}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust as needed for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_exception_handler(WrongInputException, wrong_input_handler)
app.add_exception_handler(MissingValueException, missing_value_handler)
app.add_exception_handler(OperationFailedException, operation_failed_handler)
app.add_exception_handler(NotFoundException, not_found_exception_handler)
app.add_exception_handler(DivisionByZeroException, division_by_zero_handler)
app.add_exception_handler(TokenExpiredException, token_expired_handler)
from fastapi import Request
from fastapi.responses import JSONResponse
from src.exceptions.exceptions import (
    NotFoundException, UnauthorizedException, MissingValueException, WrongInputException, OperationFailedException, ListFailedException,
    DivisionByZeroException, TokenExpiredException, WrongLoginDataException
)

async def not_found_exception_handler(request: Request, exc: NotFoundException):
    return JSONResponse(
        status_code=404,
        content={"detail": f"{exc.resource} with ID {exc.identifier} not found"}
    )

async def unauthorized_exception_handler(request: Request, exc: UnauthorizedException):
    return JSONResponse(
        status_code=403,
        content={"detail": exc.message}
    )

async def list_failed_handler(request: Request, exc: ListFailedException):
    return JSONResponse(
        status_code=500,
        content={"detail": f"{exc.message}; obj: {exc.list_object}"}
    )

async def operation_failed_handler(request: Request, exc: OperationFailedException):
    return JSONResponse(
        status_code=500,
        content={"detail": f"{exc.message}"}
    )

async def missing_value_handler(request: Request, exc: MissingValueException):
    return JSONResponse(
        status_code=404,
        content={"detail": f"{exc.missing_variable} {exc.message}"}
    )

async def wrong_input_handler(request: Request, exc: WrongInputException):
    return JSONResponse(
        status_code=400,
        content={"detail": f"Variable(s) {exc.wrong_variables} faulty; {exc.documentation}"}
    )

async def token_expired_handler(request: Request, exc: TokenExpiredException):
    return JSONResponse(
        status_code=400,
        content={"detail": exc.message}
    )

async def wrong_login_data_handler(request: Request, exc: WrongLoginDataException):
    return JSONResponse(
        status_code=400,
        content={"detail": exc.message}
    )

async def division_by_zero_handler(request: Request, exc: DivisionByZeroException):
    content=f"Division by Zero Error."
    if exc.function:
        content += f" In function: {exc.function}"
    if exc.divisor:
        content += f" {exc.divisor} should not have been zero"
    return JSONResponse(
        status_code=500,
        content={"detail": content}
    )

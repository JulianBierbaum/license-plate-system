from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute

from src.api.router import api_router
from src.logger import logger


def cstm_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"


app = FastAPI(
    title="Notification-Service",
    openapi_url="/api/openapi.json",
    generate_unique_id_function=cstm_generate_unique_id,
)

app.include_router(api_router, prefix="/api")


@app.get('/health', tags=['health'])
async def health_check():
    return {'status': 'ok'}


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Custom exception handler to log all HTTPExceptions before returning the response"""
    logger.error(
        f"HTTP Exception: {exc.status_code} - {exc.detail} for url: {request.url}"
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

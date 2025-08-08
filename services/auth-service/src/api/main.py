from fastapi import APIRouter
from src.api.routes import auth

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/login", tags=["auth"])

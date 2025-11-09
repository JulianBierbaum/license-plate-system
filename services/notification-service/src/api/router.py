from fastapi import APIRouter

from src.api.routes import user_preferences

api_router = APIRouter()

api_router.include_router(user_preferences.router, prefix='/user_preferences', tags=['user_preferences'])

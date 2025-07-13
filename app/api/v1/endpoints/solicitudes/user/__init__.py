from fastapi import APIRouter
from app.api.v1.endpoints.solicitudes.user.get import router as get_router

router = APIRouter()

router.include_router(get_router) 
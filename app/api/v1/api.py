from fastapi import APIRouter
from app.api.v1.endpoints import base
from app.api.v1.endpoints.solicitudes.user import router as user_router
from app.api.v1.endpoints.solicitudes.vet import router as vet_router

api_router = APIRouter()

# Import and include other routers here
# Example:
# from app.api.v1.endpoints import users, items
# api_router.include_router(users.router, prefix="/users", tags=["users"])
# api_router.include_router(items.router, prefix="/items", tags=["items"])

api_router.include_router(base.router, prefix="/base", tags=["base"])
api_router.include_router(user_router, prefix="/solicitudes/user", tags=["solicitudes-user"])
api_router.include_router(vet_router, prefix="/solicitudes/vet", tags=["solicitudes-vet"]) 
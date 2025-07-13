from fastapi import APIRouter
from .get import router as get_router
from .post import router as post_router
from .patch import router as patch_router
from .delete import router as delete_router

router = APIRouter()

router.include_router(get_router)
router.include_router(post_router)
router.include_router(patch_router)
router.include_router(delete_router) 
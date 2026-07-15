"""
API version 1 router.
"""

from fastapi import APIRouter

from app.api.v1.chat import router as chat_router
from app.api.v1.routes.health import router as health_router
from app.api.v1.documents import router as documents_router

router = APIRouter(
    prefix="/api/v1",
)

router.include_router(health_router)
router.include_router(chat_router)
router.include_router(documents_router)
from fastapi import APIRouter

from .api_router import router as api_router
from .common_router import router as common_router
from .music_router import router as music_router
from .websocket_router import router as websocket_router

router = APIRouter()

router.include_router(common_router)
router.include_router(api_router)
router.include_router(music_router)
router.include_router(websocket_router)

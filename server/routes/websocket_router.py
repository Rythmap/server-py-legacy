from fastapi import APIRouter
from melomap.ws import router as wsrouter

router = APIRouter(tags=["Websocket"])

router.include_router(wsrouter)


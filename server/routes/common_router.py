from fastapi import APIRouter

router = APIRouter(tags=["Common"])

@router.get("/")
async def status():
    return {"status": "ok", "version": "0.0.3"}
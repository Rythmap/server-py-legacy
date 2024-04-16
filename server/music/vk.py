import aiohttp
from fastapi import APIRouter, HTTPException, Query

router = APIRouter()

@router.get(
    "/vk.current_track",
    summary="Get current song from VK",
    description="This endpoint gets the user's current song in VK. It requires VK access_token",
)
async def get_vk_current_song(
        access_token: str = Query(..., description="VK access_token"),
):
    """
    Gets the user's current song in VK.
    Requires VK access_token.
    """
    if not access_token:
        raise HTTPException(
            status_code=400, detail="VK access_token is required"
        )

    try:
        params = {
            'access_token': access_token,
            'v': '5.199'
        }
        async with aiohttp.ClientSession() as session:
            async with session.get('https://api.vk.com/method/status.get', params=params) as response:
                response_json = await response.json()
                return response_json
    except:
        raise HTTPException(status_code=500, detail=f"Other error occurred")
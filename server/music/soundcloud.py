from fastapi import APIRouter, FastAPI, HTTPException, Query
import requests

router = APIRouter()

@router.get(
    "/soundcloud.current_track",
    summary="Get current song from SoundCloud",
    description="This endpoint gets the user's current song in SoundCloud. It requires SoundCloud client_id and oauth.",
    responses={
        400: {"description": "SoundCloud client_id and oauth required"},
        404: {"description": "No current tracks"},
        500: {"description": "Server error"},
    },
)
async def get_soundcloud_current_song(
        client_id: str = Query(..., description="SoundCloud client_id"),
        oauth: str = Query(..., description="SoundCloud oauth"),
):
    """
    Gets the user's current song in SoundCloud.
    Requires SoundCloud client_id and oauth.
    """
    if not client_id or not oauth:
        raise HTTPException(
            status_code=400, detail="SoundCloud client_id and oauth required"
        )

    soundcloud_user_url = "https://api-v2.soundcloud.com/me/play-history/tracks"
    soundcloud_headers = {"Authorization": f"OAuth {oauth}"}
    soundcloud_params = {"client_id": client_id}

    try:
        response = requests.get(
            soundcloud_user_url, params=soundcloud_params, headers=soundcloud_headers
        )
        response.raise_for_status()

        data = response.json()
        tracks_data = data.get("collection", [])
        if not tracks_data:
            raise HTTPException(status_code=404, detail="No current tracks")

        current_track = tracks_data[0]["track"] if tracks_data else "No current song"

        return current_track
    except:
        raise HTTPException(status_code=500, detail=f"Other error occurred")
from typing import Optional

from fastapi import APIRouter, HTTPException
from yandex_music import Client

router = APIRouter()


@router.get(
    "/yandex.current_track",
    summary="Get current song from Yandex Music",
    description="This endpoint gets the user's current song in Yandex Music. It requires a Yandex Music token.",
    responses={
        400: {"description": "Yandex Music token not provided"},
        404: {"description": "No current tracks"},
        500: {"description": "Server error"},
    },
)
async def get_yandex_current_song(token: Optional[str] = None):
    """
    Gets the user's current song in Yandex Music.
    Requires a Yandex Music token.
    """
    yandex_token = token
    if yandex_token:
        try:
            yandex_client = Client(yandex_token).init()
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to initialize Yandex client: {str(e)}"
            )
        try:
            all_queues = yandex_client.queues_list()
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to list queues: {str(e)}"
            )
        if all_queues:
            try:
                latest_queue = yandex_client.queue(all_queues[0].id)
                current_track_id = latest_queue.get_current_track()
                current_track = current_track_id.fetch_track().to_dict()
                return current_track
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Failed to fetch track: {str(e)}"
                )
        else:
            raise HTTPException(status_code=404, detail="No current tracks")
    else:
        raise HTTPException(status_code=400, detail="Yandex Music token not provided")

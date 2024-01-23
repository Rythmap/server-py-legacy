from fastapi import APIRouter
from typing import Optional
from fastapi import HTTPException, FastAPI, Query


router = APIRouter()

@router.get("/spotify.current_track")
async def spotify_auth():
    scope = ["user-read-currently-playing"]
    auth_url = f"https://accounts.spotify.com/authorize?response_type=code&client_id={spotify_client_id}&redirect_uri={spotify_redirect_uri}&scope={' '.join(scope)}"
    return {"auth_url": auth_url}


@router.get("/spotify/callback")
async def spotify_callback(code):
    headers = get_spotify_access_token(code)

    url = f"https://api.spotify.com/v1/me/player/currently-playing"
    response = requests.get(url=url, headers=headers)

    if response.status_code == 200:
        return {"current_track": response.json()}
    else:
        return {"error": response.json()}


def get_spotify_access_token(auth_code: str):
    response = requests.post(
        "https://accounts.spotify.com/api/token",
        data={
            "grant_type": "authorization_code",
            "code": auth_code,
            "redirect_uri": spotify_redirect_uri,
        },
        auth=(spotify_client_id, spotify_client_secret),
    )
    print(response.text)
    access_token = response.json()["access_token"]
    return {"Authorization": "Bearer " + access_token}
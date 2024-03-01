from fastapi import APIRouter
from music.soundcloud import router as soundcloud
from music.spotify import router as spotify
from music.yandex import router as yandex

router = APIRouter(tags=["Music"])

music_prefix = "/music"

router.include_router(soundcloud, prefix=music_prefix)
router.include_router(spotify, prefix=music_prefix)
router.include_router(yandex, prefix=music_prefix)


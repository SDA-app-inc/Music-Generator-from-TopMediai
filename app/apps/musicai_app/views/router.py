from fastapi import APIRouter

from app.apps.musicai_app.views.media_processing import router as media_router
from app.apps.musicai_app.views.top_media_processing import router as top_media_router
from app.apps.musicai_app.views.voice import router as voice_router
media_generation_module_router = APIRouter(
    tags=["Media Generation"],
)

media_generation_module_router.include_router(
    media_router,
)

top_media_generation_module_router = APIRouter(
    tags=["Top Media Generation"],
)
top_media_generation_module_router.include_router(
    top_media_router,
)

voice_generation_module_router = APIRouter(
    tags=["Voice Generation"],
)
voice_generation_module_router.include_router(
    voice_router,
)
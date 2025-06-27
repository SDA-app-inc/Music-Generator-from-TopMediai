from fastapi import APIRouter

from app.apps.musicai_app.views.router import (media_generation_module_router,
                                           top_media_generation_module_router,voice_generation_module_router)

router = APIRouter()

router.include_router(media_generation_module_router)
router.include_router(top_media_generation_module_router)
router.include_router(voice_generation_module_router)
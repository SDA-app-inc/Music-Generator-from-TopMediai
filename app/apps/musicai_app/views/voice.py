from fastapi import APIRouter
from fastapi.params import Query

from app.apps.musicai_app.services.infrastructure_services.voice_service import VoiceService
router = APIRouter()


@router.get("/",)
async def get_voices(
    limit: int = Query(20, ge=1, le=100, description="Максимум 100 записей за раз"),
    offset: int = Query(0, ge=0, description="Смещение для пагинации"),
):
    """
    📄 Получить список голосов с пагинацией
    """
    voices = VoiceService.get_voice_service(limit=limit, offset=offset)
    return voices
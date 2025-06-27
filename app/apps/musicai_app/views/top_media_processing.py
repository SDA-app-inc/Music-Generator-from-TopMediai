from fastapi import APIRouter

from app.apps.musicai_app.schemas.requests.audio_processing_schema import \
     SpeechSynthesisPayloadSchema, SongGenerationPayloadSchema
from app.apps.musicai_app.services.business_services.download_music import download_music

from app.apps.musicai_app.services.business_services.top_media_music_generator import generate_top_media_music
from app.apps.musicai_app.services.business_services.top_media_text2spech import generate_text2speech

router = APIRouter()


@router.post("/media/generate_text2speech")
async def generate_speech_view(
        app_bundle_id: str,
        user_id: str,
        data: SpeechSynthesisPayloadSchema,
):
    response = await generate_text2speech(data=data, app_bundle_id=app_bundle_id, user_id=user_id)
    return response


@router.post("/media/generate_music")
async def generate_top_media_music_view(
        app_bundle_id: str,
        user_id: str,
        data: SongGenerationPayloadSchema,
):
    response = await generate_top_media_music(data=data, app_bundle_id=app_bundle_id, user_id=user_id)
    return response


@router.get("/download")
def download_music_view(title: str):
    return  download_music(title)


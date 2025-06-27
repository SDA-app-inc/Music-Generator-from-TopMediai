from fastapi import APIRouter

from app.apps.musicai_app.schemas.requests.audio_processing_schema import GenerateTextToSpeechRequestSchema, \
    SoundGenerationRequestSchema
from app.apps.musicai_app.services.business_services.generate_music import generate_music_from_text
from app.apps.musicai_app.services.business_services.generate_text_to_speech import generate_text_to_speech

router = APIRouter()


@router.post("/audio/generate_speech", include_in_schema=False
             )
async def generate_audio_speech_view(
        app_bundle_id: str,
        user_id: str,
        body: GenerateTextToSpeechRequestSchema,
):
    response = await generate_text_to_speech(body, app_bundle_id, user_id)
    return response


@router.post("/audio/generate_sound", include_in_schema=False)
async def generate_music_from_text_view(
        app_bundle_id: str,
        body: SoundGenerationRequestSchema,
):
    response = await generate_music_from_text(body, app_bundle_id)
    return response

import os
from io import BytesIO

from starlette.responses import StreamingResponse

from app.apps.musicai_app.schemas.requests.audio_processing_schema import GenerateTextToSpeechRequestSchema, \
    SoundGenerationRequestSchema
from app.utils.elevenlabs_client import ElevenLabsClient
from app.apps.musicai_app.services.infrastructure_services.application_statistics_service import \
    ApplicationStatisticsService
from app.configs import settings


async def generate_text_to_speech(
        body: SoundGenerationRequestSchema,
        app_bundle_id: str,
        user_id: str,
        eleven_labs_client: ElevenLabsClient = ElevenLabsClient(api_key=os.getenv('ELEVEN_LABS_API_KEY'),
                                                                proxy_url=settings.PROXY_URL),
        application_statistic_service: ApplicationStatisticsService = ApplicationStatisticsService()
):
    await application_statistic_service.save_request_stat(app_id=app_bundle_id, user_id=user_id)
    audio_bytes = await eleven_labs_client.text_to_speech(body.text, body.voice_id)

    audio_stream = BytesIO(audio_bytes)
    audio_metadata = {
        "filename": "speech.mp3",
        "file_type": "audio/mp3",
    }
    return StreamingResponse(audio_stream, media_type="audio/mp3", headers={
        "Content-Disposition": f"attachment; filename={audio_metadata['filename']}"
    })

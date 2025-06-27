import os
from io import BytesIO

from starlette.responses import StreamingResponse

from app.apps.musicai_app.schemas.requests.audio_processing_schema import GenerateTextToSpeechRequestSchema
from app.configs import settings
from app.utils.elevenlabs_client import ElevenLabsClient


async def generate_music_from_text(
        body: GenerateTextToSpeechRequestSchema,
        app_bundle_id: str,
        eleven_labs_client: ElevenLabsClient = ElevenLabsClient(api_key=os.getenv('ELEVEN_LABS_API_KEY'),
                                                                proxy_url=settings.PROXY_URL),
):
    sound_effect = await eleven_labs_client.text_to_sound_effects(body.text)
    sound_effect_stream = BytesIO(sound_effect)

    audio_metadata = {
        "filename": "sound.mp3",
        "file_type": "audio/mp3",
    }
    return StreamingResponse(sound_effect_stream, media_type="audio/mp3", headers={
        "Content-Disposition": f"attachment; filename={audio_metadata['filename']}"
    })
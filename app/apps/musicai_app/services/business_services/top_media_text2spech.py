import os

from fastapi import HTTPException

from app.apps.musicai_app.schemas.requests.audio_processing_schema import SpeechSynthesisPayloadSchema
from app.exceptions import TopMediaAPIError
from app.utils.top_media_client import TopMediaClient
from app.apps.musicai_app.services.infrastructure_services.application_statistics_service import \
    ApplicationStatisticsService


async def generate_text2speech(
        app_bundle_id: str,
        user_id: str,
        data: SpeechSynthesisPayloadSchema,
        top_media_ai_client: TopMediaClient = TopMediaClient(api_key=os.environ.get("TOP_MEDIA_API_KEY")),
        application_statistic_service: ApplicationStatisticsService = ApplicationStatisticsService()

):
    await application_statistic_service.save_request_stat(app_id=app_bundle_id, user_id=user_id)

    try:
        result = await top_media_ai_client.text_to_speech(data.text, data.speaker, data.emotion)
        return {
            "message": "Speech",
            "data": result
        }
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except TopMediaAPIError as e:
        raise HTTPException(status_code=502, detail=f"TopMedia error: {e.message}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected server error: {str(e)}")

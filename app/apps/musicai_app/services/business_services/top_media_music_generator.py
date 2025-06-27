import os

from fastapi import HTTPException, status

from app.apps.musicai_app.schemas.requests.audio_processing_schema import SongGenerationPayloadSchema
from app.apps.musicai_app.services.infrastructure_services.application_statistics_service import \
    ApplicationStatisticsService
from app.apps.musicai_app.services.infrastructure_services.music_generator_service import generate_unique_title
from app.utils.top_media_client import TopMediaClient
from app.utils.top_media_parser import TopMediaIAgent


async def generate_top_media_music(
        app_bundle_id: str,
        user_id: str,
        data: SongGenerationPayloadSchema,
        top_media_ai_client: TopMediaClient = TopMediaClient(api_key=os.environ.get("TOP_MEDIA_API_KEY")),
        application_statistic_service: ApplicationStatisticsService = ApplicationStatisticsService()

):

    await application_statistic_service.save_request_stat(app_id=app_bundle_id, user_id=user_id)
    try:
        unique_title = generate_unique_title()

        try:
            response = await top_media_ai_client.generate_music(
                lyrics=data.lyrics,
                title=unique_title,
            )
        except Exception as e:
            if "not authorized" in str(e).lower():
                # Повторный логин
                agent = TopMediaIAgent()
                try:
                    agent.login_if_needed()
                finally:
                    agent.stop()

                # Повторный запрос
                response = await top_media_ai_client.generate_music(
                    lyrics=data.lyrics,
                    title=unique_title,
                )
            else:
                raise e

        return {
            "tracks": response,
            "unique_title": unique_title
        }
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"⚠️ Не удалось сгенерировать музыку: {str(e)}")

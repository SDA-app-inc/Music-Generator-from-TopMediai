from app.database import sync_session
from app.models.request_stats import RequestStats


class ApplicationStatisticsService:
    @classmethod
    async def save_request_stat(
            cls,
            app_id: str,
            user_id: str
    ):
        with sync_session() as session:
            stat = RequestStats(
                app_id=app_id,
                user_id=user_id,
            )
            session.add(stat)
            session.commit()
            session.refresh(stat)
            return stat

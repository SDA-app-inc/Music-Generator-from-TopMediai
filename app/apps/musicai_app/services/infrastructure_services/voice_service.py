from app.database import sync_session
from app.models.voice import Voice


class VoiceService:

    @classmethod
    def get_voice_service(cls, limit: int = 20, offset: int = 0):
        with sync_session() as session:
            results = session.query(Voice) \
                .offset(offset) \
                .limit(limit) \
                .all()
            return results

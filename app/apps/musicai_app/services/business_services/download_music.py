from http.client import HTTPException

from fastapi.responses import FileResponse
import os

from app.utils.top_media_parser import TopMediaIAgent

BASE_DIR = os.path.dirname(__file__)  # путь к текущему файлу
DOWNLOADS_DIR = os.path.join(BASE_DIR, "utils", "downloads")

def download_music(title: str):
    agent = TopMediaIAgent()
    try:
        agent.login_if_needed()
        file_path = agent.get_music_save(title)
    finally:
        agent.stop()

    if not file_path or not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Файл не найден")

    return FileResponse(
        path=file_path,
        filename=os.path.basename(file_path),
        media_type="audio/mpeg"
    )


import logging
import os
import subprocess
import sys
from contextlib import asynccontextmanager

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI
from sqladmin import Admin
from app.admin.admin import TemplateAdminView, RequestStatsAdminView, ApplicationAdminView

load_dotenv()

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import engine
from app.apps.router import router

logging.basicConfig(level=logging.INFO)

import logging
import subprocess
import os


def run_migrations():
    try:
        current_dir = os.path.abspath(os.path.dirname(__file__))

        # Путь до alembic.ini на уровень выше
        alembic_cfg_path = os.path.join(current_dir, "..", "alembic.ini")

        if not os.path.isfile(alembic_cfg_path):
            raise FileNotFoundError(f"alembic.ini not found at: {alembic_cfg_path}")

        logging.info(f"🧭 Используем alembic.ini: {alembic_cfg_path}")

        # Запускаем Alembic
        result = subprocess.run(
            ["alembic", "-c", alembic_cfg_path, "upgrade", "head"],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(alembic_cfg_path),
            env={**os.environ}  # передаём переменные окружения

        )

        if result.returncode != 0:
            logging.error(f"Alembic upgrade failed:\nSTDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}")
            raise RuntimeError("Alembic migration failed")

        logging.info("✅ Alembic миграции успешно применены")
    except Exception as e:
        logging.error(f"❌ Ошибка при миграции: {e}")
        raise


@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.info("Запуск приложения...")

    try:
        logging.info("Запуск Alembic миграций...")
        run_migrations()  # Запуск миграций
        yield
    except Exception as e:
        logging.error(f"Ошибка при запуске приложения: {e}")
        raise
    finally:
        logging.info("Завершение работы приложения.")


def init():
    app = FastAPI(
        title="MusicAI",
        version="1.0.0",
        lifespan=lifespan,
    )
    app.include_router(prefix="/v1", router=router)
    # Настроим админку
    admin = Admin(app, engine, title='MusicAI')
    admin.add_view(TemplateAdminView)
    admin.add_view(ApplicationAdminView)
    admin.add_view(RequestStatsAdminView)

    logging.info("Запуск FastAPI сервера...")
    return app


if __name__ == "__main__":
    app = init()
    uvicorn.run(app, host='0.0.0.0', port=38046)

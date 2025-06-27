from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.configs import settings

# Создание синхронного движка
engine = create_engine(
    settings.DATABASE_URL_psycopg,
    echo=True,
    pool_size=5,
    max_overflow=10,
)

# Фабрика сессий для работы с синхронными соединениями
sync_session = sessionmaker(
    bind=engine,
    expire_on_commit=False,
)

class Base(DeclarativeBase):
    pass

# Синхронная функция для проверки версии базы данных
def check_version():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT VERSION()"))
        version = result.scalar_one()
        print(f"Postgres version: {version}")

# Запуск проверки версии
if __name__ == "__main__":
    check_version()

import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    POSTGRES_USER: str = os.getenv('POSTGRES_USER')
    POSTGRES_PASS: str = os.getenv('POSTGRES_PASS')
    POSTGRES_HOST: str = os.getenv('POSTGRES_HOST')
    POSTGRES_PORT: int = os.getenv('POSTGRES_PORT')
    POSTGRES_NAME: str = os.getenv('POSTGRES_NAME')

    POSTGRES_CONN_TIMEOUT: int = 60
    POSTGRES_MIN_CONN_SIZE: int = 1
    POSTGRES_MAX_CONN_SIZE: int = 10

    PROXY_USER: str = os.getenv('PROXY_USER')
    PROXY_PASS: str = os.getenv('PROXY_PASS')
    PROXY_IP: str = os.getenv('PROXY_IP')
    PROXY_PORT: int = os.getenv('PROXY_PORT')
    print(PROXY_PASS, PROXY_IP, PROXY_PORT)

    @property
    def PROXY_URL(self) -> str:
        proxy_url = f"socks5://{self.PROXY_USER}:{self.PROXY_PASS}@{self.PROXY_IP}:{self.PROXY_PORT}"
        return proxy_url

    @property
    def DATABASE_URL_psycopg(self):
        # DSN https://www.fastapitutorial.com/blog/database-connection-fastapi/ example
        # database_url = "postgresql+psycopg://hovo:password@localhost:5432/music_ai_2"
        # return database_url
        return (
            f"postgresql+psycopg://"
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASS}@"
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/"
            f"{self.POSTGRES_NAME}"
        )


settings = Settings()

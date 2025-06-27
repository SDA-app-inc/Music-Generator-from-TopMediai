import httpx
from typing import Dict
# from app.utils.proxy import ProxyHandler


class ElevenLabsClient:
    def __init__(self, api_key: str, proxy_url: str | None = None,
                 base_url: str = "https://api.elevenlabs.io/v1"):
        """
        Инициализация асинхронного клиента ElevenLabs с поддержкой SOCKS5-прокси.
        :param api_key: Ключ API для доступа.
        :param proxy_url: URL прокси-сервера
        :param base_url: Базовый URL для API (по умолчанию https://api.elevenlabs.io/v1).
        """
        self.api_key = api_key
        self.base_url = base_url
        self.proxy_url = proxy_url
        # self.proxy_handler = ProxyHandler(proxy_url)

    async def _send_request(self, endpoint: str, data: Dict[str, str]) -> bytes:
        """Общий асинхронный метод для отправки POST-запросов с прокси."""
        url = f"{self.base_url}/{endpoint}"
        headers = {
            "xi-api-key": self.api_key,
            "Content-Type": "application/json"
        }

        # proxies = self.proxy_handler.get_proxies()

        async with httpx.AsyncClient(proxy=self.proxy_url) as client:
            response = await client.post(url, headers=headers, json=data)

        if response.status_code == 200:
            return response.content
        else:
            raise Exception(f"Error {response.status_code}: {response.text}")

    async def text_to_speech(self, text: str, voice_id: str | None = None,
                             model_id: str = "eleven_multilingual_v2",
                             output_format: str = "mp3_44100_128", ) -> bytes:
        """
        Асинхронная генерация речи из текста.
        :param voice_id:
        :param text: Текст для генерации речи.
        :param model_id: Идентификатор модели для синтеза речи (по умолчанию "eleven_multilingual_v2").
        :param output_format: Формат аудио (по умолчанию "mp3_44100_128").
        :return: Аудиофайл в формате mp3.
        """
        voice_id = voice_id or "JBFqnCBsd6RMkjVDRZzb"
        endpoint = f"text-to-speech/{voice_id}"
        data = {
            "text": text,
            "model_id": model_id,
            "output_format": output_format,
            "voice_id": voice_id
        }
        return await self._send_request(endpoint, data)

    async def text_to_sound_effects(self, text: str) -> bytes:
        """
        Асинхронная генерация звуковых эффектов из текста.
        :param text: Текст для генерации звукового эффекта.
        :return: Звуковой эффект в формате mp3.
        """
        endpoint = "sound-generation"
        data = {
            "text": text
        }
        return await self._send_request(endpoint, data)

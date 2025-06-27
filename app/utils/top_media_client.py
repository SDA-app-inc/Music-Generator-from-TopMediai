import os
from typing import Any, Dict, Optional, Union
import httpx

class InsufficientCreditsError(Exception):
    """Вызывается, если у пользователя закончились кредиты."""
    pass


class TopMediaClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = 'https://api.topmediai.com'

    async def _send_request(
            self,
            endpoint: str,
            data: Dict[str, Any],
            headers_2: Optional[Dict[str, Any]] = None,
            full_url: bool = False
    ) -> Dict[str, Any]:
        url = endpoint if full_url else f"{self.base_url}/{endpoint}"
        headers = {
            "Content-Type": "application/json",
            "x-api-key": self.api_key
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    url,
                    headers=headers_2 if headers_2 else headers,
                    json=data
                )
                response.raise_for_status()
                result = response.json()
                print(result)
                if isinstance(result, dict):
                    if result.get("status") == 400 and "left counts" in result.get("message", ""):
                        raise InsufficientCreditsError("❗ Недостаточно кредитов для выполнения запроса.")
                    return result
                else:
                    raise Exception("❌ Неверный формат ответа от API.")
            except httpx.HTTPStatusError as e:
                raise Exception(f"❌ Ошибка запроса: {e.response.status_code} — {e.response.text}")
            except Exception as e:
                raise Exception(f"❗ Неизвестная ошибка при запросе: {str(e)}")

    async def text_to_speech(
        self,
        text: str,
        speaker_id: str,
        emotion: Optional[str] = None
    ) -> Dict[str, Any]:
        payload = {
            "text": text,
            "speaker": speaker_id
        }
        if emotion:
            payload["emotion"] = emotion

        return await self._send_request("v1/text2speech", payload)

    async def generate_music(
            self,
            lyrics: str,
            title: str,
            # instrumental: str|None = None,

    ) -> Dict[str, Any]:
        url = "https://aimusic-api.topmediai.com/v2/async/text-to-song"

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0"
        }
        token = os.getenv("TOPMEDIAI_TOKEN")
        if not token:
            raise Exception("❌ Токен не найден. Выполни вход через TopMediaIAgent")

        payload = {
            "mv": "v4.0",
            "is_public": "1",
            "instrumental": "0",
            "action": "custom",
            "style": "Piano",
            "lyrics": lyrics,
            "title": title,
            "gender": "male",
            "token": token
        }

        async with httpx.AsyncClient(timeout=30) as client:
            try:
                response = await client.post(url, data=payload, headers=headers)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                raise Exception(f"❌ HTTP ошибка: {e.response.status_code} — {e.response.text}")
            except Exception as e:
                raise Exception(f"❗ Ошибка при запросе: {str(e)}")

    async def generate_ai_cover(self):
        raise NotImplementedError("🔧 Метод generate_ai_cover еще не реализован.")

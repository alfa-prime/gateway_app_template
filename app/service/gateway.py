import httpx
from fastapi import HTTPException

from app.core import get_settings, logger


class GatewayService:
    settings = get_settings()
    GATEWAY_ENDPOINT = settings.GATEWAY_REQUEST_ENDPOINT

    def __init__(self, client: httpx.AsyncClient):
        self._client = client

    async def make_request(self, payload: dict) -> dict:
        try:
            response = await self._client.post(self.GATEWAY_ENDPOINT, json=payload)
            response.raise_for_status()
            return response.json()

        except httpx.RequestError as exc:
            logger.exception(f"Не удалось подключиться к шлюзу: {exc}")
            raise HTTPException(status_code=503, detail=f"Не удалось подключиться к шлюзу: {exc}")
        except httpx.HTTPStatusError as exc:
            logger.exception(f"Ошибка от шлюза: {exc.response.text}")
            raise HTTPException(status_code=exc.response.status_code, detail=f"Ошибка от шлюза: {exc.response.text}")

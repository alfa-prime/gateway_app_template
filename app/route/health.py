# app/route/health.py

from typing import Annotated

import httpx
from fastapi import APIRouter, Depends, HTTPException

from app.core import get_gateway_service, get_api_key
from app.service import GatewayService

router = APIRouter(prefix="/health", tags=["Health Check"], dependencies=[Depends(get_api_key)])


@router.get(
    "/",
    summary="Стандартная проверка работоспособности",
    description="Возвращает 'pong', если сервис запущен и отвечает на запросы."
)
async def check():
    """Простая проверка работоспособности сервиса."""
    return {"ping": "pong"}


@router.post(
    "/gateway",
    summary="Проверка связи со шлюзом API",
    description="Отправляет тестовый запрос на API-шлюз для проверки связи и аутентификации."
)
async def check_gateway_connection(
        gateway_service: Annotated[GatewayService, Depends(get_gateway_service)]
):
    payload = {
        "params": {
            "c": "Common",
            "m": "getCurrentDateTime"
        },
        "data": {
            "is_activerulles": "true"
        }
    }

    try:
        response = await gateway_service.make_request(payload)
        return response


    except httpx.RequestError as exc:
        raise HTTPException(status_code=503, detail=f"Не удалось подключиться к шлюзу: {exc}")

    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=f"Ошибка от шлюза: {exc.response.text}")

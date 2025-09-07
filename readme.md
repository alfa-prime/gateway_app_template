# Шаблон приложения для шлюза ЕВМИАС API

Этот репозиторий представляет собой готовый шаблон для быстрой разработки приложений, взаимодействующих со шлюзом ЕВМИАС API. Он включает в себя настроенный HTTP-клиент для отправки запросов и механизм авторизации по API-ключу.

В качестве примера реализован роут `/health`, демонстрирующий проверку связи со шлюзом.

---

## Требования

Перед началом работы убедитесь, что у вас установлены:

- Git  
- Docker  
- Docker Compose  

---

## Быстрый старт

### 1. Клонирование репозитория

Клонируйте репозиторий в папку с желаемым именем вашего проекта (например, `my_super_app`).

```bash
git clone ssh://git@gitverse.ru:2222/imperium/gateway_app_template.git my_super_app
```

Если не указать `my_super_app`, проект будет склонирован в папку `gateway_app_template`.

---

### 2. Настройка конфигурации

Скопируйте файл с примером переменных окружения.

```bash
# Перейдите в папку проекта
cd my_super_app

# Скопируйте .env.example в .env
cp .env.example .env
```

**Откройте файл `.env` и настройте его под ваш проект:**

`GATEWAY_API_KEY`: Укажите ваш ключ доступа к шлюзу.

`DEV_CONTAINER_NAME` и `PROD_CONTAINER_NAME`: Задайте уникальные имена для контейнеров.

`DEV_PORT` и `PROD_PORT`: При необходимости измените порты, по которым приложение будет доступно.


```dotenv
# .env
GATEWAY_URL=http://192.168.0.249:8777/
GATEWAY_API_KEY=ваш-реальный-ключ-доступа
GATEWAY_REQUEST_ENDPOINT=gateway/request

# Имена контейнеров
DEV_CONTAINER_NAME=my_super_app
PROD_CONTAINER_NAME=my_super_app_prod

# Порты для доступа с хост-машины
DEV_PORT=8000
PROD_PORT=8778
```

### 3. Запуск приложения

**Для разработки (с live-reload):**

```bash
make up
```
Приложение будет доступно по адресу:  
👉 [http://localhost:8000](http://localhost:8000)

**Для продакшена:**

```bash
make up-prod
```
Приложение будет доступно по адресу:  
👉 [http://localhost:8778](http://localhost:8778)

---

## Доступные команды (makefile)

### Разработка

| Команда     | Описание |
|-------------|----------|
| `make up`   | Собрать и запустить контейнер в режиме разработки. |
| `make down` | Остановить и удалить контейнер разработки. |
| `make bash` | Открыть интерактивную сессию bash внутри контейнера. |

### Продакшен

| Команда         | Описание |
|-----------------|----------|
| `make up-prod`  | Собрать и запустить контейнер в фоновом режиме (production). |
| `make down-prod`| Остановить и удалить контейнер продакшена. |
| `make logs-prod`| Показать и отслеживать логи работающего приложения. |
| `make bash-prod`| Открыть интерактивную сессию bash внутри prod-контейнера. |

### Общие

| Команда      | Описание |
|--------------|----------|
| `make clean` | Удалить все неиспользуемые Docker-образы, контейнеры, тома и сети. |

---

## GatewayService

Для любого взаимодействия со шлюзом ЕВМИАС в проекте предназначен `GatewayService`.  
Его можно легко получить в любом роутере через систему зависимостей **FastAPI**.  
Все запросы сервис отправляет на единый эндпоинт, указанный в `.env` файле (`GATEWAY_REQUEST_ENDPOINT`).

Сервис имеет один универсальный метод для выполнения запросов:

```python
make_request(method: str, **kwargs)
```

### Аргументы метода

- **method**: HTTP-метод в виде строки (`'post'`, `'get'`, `'put'` и т.д.).  
- **kwargs**: Любые именованные аргументы, которые принимает HTTP-клиент **httpx**.  
  Самые важные из них:
  - `json=<dict>` — для передачи тела запроса (используется в `POST`, `PUT`, `PATCH`).
  - `params=<dict>` — для передачи query-параметров в URL (используется в `GET`).

---

### Пример 1: POST-запрос (самый частый случай)

```python
# В вашем файле с роутерами, например, app/route/my_new_route.py
from fastapi import APIRouter, Depends
from app.core import get_gateway_service
from app.service import GatewayService
from typing import Annotated

router = APIRouter(prefix="/entities", tags=["Entities"])

@router.post("/")
async def create_entity(
    gateway_service: Annotated[GatewayService, Depends(get_gateway_service)]
):
    payload = {
        "params": {"c": "SomeClass", "m": "someMethod"},
        "data": {"name": "New Entity", "value": 123}
    }
    
    # Вызываем сервис, указывая метод 'post' и передавая данные через 'json'
    response_data = await gateway_service.make_request('post', json=payload)
    
    return response_data
```

---

### Пример 2: GET-запрос с параметрами

```python
# ... (импорты те же)

@router.get("/")
async def get_entities_list(
    gateway_service: Annotated[GatewayService, Depends(get_gateway_service)]
):
    query_params = {
        "entity_type": "user",
        "status": "active"
    }
    
    # Вызываем сервис с методом 'get' и передавая параметры через 'params'
    response_data = await gateway_service.make_request('get', params=query_params)
    
    return response_data
```



## Тестовый эндпоинт (/health)

Для проверки работоспособности сервиса и связи со шлюзом используйте следующие эндпоинты.  
Не забудьте передать ваш `X-API-KEY` в заголовках.

### Проверка работоспособности сервиса

**Запрос:**

```bash
curl -X GET http://localhost:8000/health/   -H "X-API-KEY: ваш-реальный-ключ-доступа"
```

**Успешный ответ:**

```json
{
  "ping": "pong"
}
```

---

### Проверка связи со шлюзом ЕВМИАС

**Запрос:**

```bash
curl -X POST http://localhost:8000/health/gateway   -H "X-API-KEY: ваш-реальный-ключ-доступа"
```

**Успешный ответ:**

Ответ будет содержать данные, полученные от шлюза (например, текущее время на сервере шлюза).

```json
{
  "data": {
    "current_datetime": "2024-09-07T12:00:00.000Z"
  },
  "success": true
}
```

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.route import health_router
from app.core import init_gateway_client, shutdown_gateway_client

tags_metadata = []

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_gateway_client(app)
    yield
    await shutdown_gateway_client(app)

app = FastAPI(
    tags = tags_metadata,
    title = "Шаблон приложения для работы со шлюзом ЕВМИАС API",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,  # noqa
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)

from contextlib import asynccontextmanager

from fastapi import FastAPI, staticfiles
from prometheus_fastapi_instrumentator import Instrumentator

from source.auth.router import router as auth_router
from source.front.router import router as front_router
from source.logger_setup import LoggingMiddleware, setup_loggers
from source.messages.router import router as messages_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_loggers("logging_config.json")
    yield


app = FastAPI(
    debug=True,
    title="Anonym messages",
    description="Сайт для анонимных для отправки анонимных сообщений",
    lifespan=lifespan,
)

app.include_router(router=auth_router, prefix="/api")
app.include_router(router=messages_router, prefix="/api")
app.include_router(router=front_router)

app.mount("/static", staticfiles.StaticFiles(directory="source/static"), name="static")

app.add_middleware(LoggingMiddleware)

instrumentator = Instrumentator().instrument(app).expose(app)

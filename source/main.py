from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

from source.auth.router import router as auth_router
from source.exceptions import config_app
from source.messages.router import router as messages_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    debug=True,
    title="Anonym messages",
    description="Сайт для анонимных для отправки анонимных сообщений",
    lifespan=lifespan,
)


@app.get(
    "/",
    description="Основная страница с описанием и приглашением для регистрации",
)
def main_page(request: Request):
    return {"content": "Это главная страница"}


app.include_router(router=auth_router)
app.include_router(router=messages_router)

config_app.bind_auth_exc_handlers_with_app(app)
config_app.bind_messages_exc_handlers_with_app(app)

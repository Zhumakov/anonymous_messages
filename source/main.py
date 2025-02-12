from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, staticfiles

from source.auth.router import router as auth_router
from source.exceptions import config_app
from source.front.router import router as front_router
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

app.include_router(router=auth_router)
app.include_router(router=messages_router)
app.include_router(router=front_router)

config_app.bind_auth_exc_handlers_with_app(app)
config_app.bind_messages_exc_handlers_with_app(app)

app.mount("/static", staticfiles.StaticFiles(directory="source/static"), name="static")

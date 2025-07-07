"""Этот модуль создаёт класс с настройками для проекта."""

from typing import Literal

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Класс с настройками проекта."""

    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    MODE: Literal["DEV", "TEST", "PROD"]

    POSTGRES_DB: str
    POSTGRES_HOST: str
    POSTGRES_PASSWORD: str
    POSTGRES_PORT: int
    POSTGRES_USER: str

    GF_SECURITY_ADMIN_USER: str
    GF_SECURITY_ADMIN_PASSWORD: str

    ALGORITHM: str
    SECRET_KEY: str


settings = Settings()

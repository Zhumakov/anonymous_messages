"""Этот модуль создаёт класс с настройками для проекта."""

from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Класс с насройками проекта."""

    LOG_LEVEL = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
    MODE = Literal["DEV", "TEST", "PROD"]

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

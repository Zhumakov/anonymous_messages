"""Этот модуль создаёт класс с настройками для проекта."""   


from typing import Literal

from pydantic import BaseConfig


class Settings(BaseConfig):
    """Класс с насройками проекта."""

    LOG_LEVEL = Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
    MODE = Literal['DEV', 'TEST', 'PROD']

    class Config:
        env_file = '.env'

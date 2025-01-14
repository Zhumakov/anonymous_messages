import os

from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,

)
from sqlalchemy.orm import DeclarativeBase

from source.settings import settings


if settings.MODE == "TEST":
    DATABASE_URL = (
        f"postgresql+asyncpg://"
        f"{settings.TEST_DB_USER}:{settings.TEST_DB_PASS}"
        f"@{settings.TEST_DB_HOST}:{settings.TEST_DB_PORT}/{settings.TEST_DB_NAME}"
    )
    DATABASE_PARAMS = {"poolclass": NullPool, "echo": True}

else:
    DATABASE_URL = (
            f"postgresql+asyncpg://"
            f"{settings.DB_USER}:{settings.DB_PASS}"
            f"@{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
            )
    DATABASE_PARAMS = {}

os.environ["SQLALCHEMY_URL"] = DATABASE_URL

async_engine = create_async_engine(url=DATABASE_URL, **DATABASE_PARAMS, future=True)
async_session = async_sessionmaker(
    bind=async_engine, expire_on_commit=False, class_=AsyncSession
)


class Base(DeclarativeBase):
    pass


async def get_session():
    async with async_session() as session:
        yield session

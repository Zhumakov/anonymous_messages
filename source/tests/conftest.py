"""This module contains prepared fixture for functional test for async requests."""

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import Insert
from sqlalchemy.ext.asyncio import AsyncSession

from source.auth.models import Users
from source.database_service.Base import Base
from source.database_service.database_config import (
    DATABASE_PARAMS,
    DATABASE_URL,
    create_async_engine,
    async_engine,
    session_maker
)
from source.main import app as FastApi_app
from source.settings import settings


@pytest.fixture(scope="session")
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=FastApi_app), base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session", autouse=True)
async def init_database():
    assert settings.MODE == "TEST"

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with session_maker() as session:
        session: AsyncSession
        query = Insert(Users).values(
            {
                "username": "logintest",
                "email": "logintest@gmail.com",
                "hashed_password": "pasword",
            }
        )
        await session.execute(query)
        await session.commit()

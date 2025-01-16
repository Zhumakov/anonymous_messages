"""This module contains prepared fixture for functional test for async requests."""

import pytest
from httpx import ASGITransport, AsyncClient

from source.main import app as FastApi_app
from source.database_service.database_config import async_engine
from source.database_service.Base import Base
from source.settings import settings


@pytest.fixture(scope="session")
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=FastApi_app), base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="module")
async def init_database():
    assert settings.MODE == "TEST"

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

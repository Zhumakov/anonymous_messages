"""This module contains prepared fixture for functional test for async requests."""

import json
from datetime import UTC, datetime

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import Insert
from sqlalchemy.ext.asyncio import AsyncSession

from source.auth.dependenties import get_current_user
from source.auth.models import User
from source.database_service.Base import Base
from source.database_service.database_config import async_engine, session_maker
from source.main import app as FastApi_app
from source.messages.models import Message
from source.messages.router import DATETIME_FORMAT
from source.settings import settings


def open_json_mock(model: str):
    with open(f"source/tests/mock_{model}.json") as file:
        return json.load(file)


FIXED_DATETIME = datetime(2025, 5, 5, 0, 0, 0, 0, tzinfo=UTC)
FIXED_STR_DATETIME = FIXED_DATETIME.strftime(DATETIME_FORMAT)
USERS = open_json_mock("user")
MESSAGES = open_json_mock("message")
for message in MESSAGES:
    message["sended_date"] = FIXED_DATETIME


@pytest.fixture(scope="session")
async def async_client():
    async with AsyncClient(
        transport=ASGITransport(app=FastApi_app), base_url="http://test"
    ) as ac:
        yield ac


@pytest.fixture(scope="module", autouse=True)
async def init_database():
    assert settings.MODE == "TEST"

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with session_maker() as session:
        session: AsyncSession
        add_users = Insert(User).values(USERS)
        add_messages = Insert(Message).values(MESSAGES)

        await session.execute(add_users)
        await session.execute(add_messages)

        await session.commit()


@pytest.fixture(scope="function")
async def auth_async_client():
    async with AsyncClient(
        transport=ASGITransport(app=FastApi_app), base_url="http://test"
    ) as ac:
        login_url = FastApi_app.url_path_for("login_user")
        await ac.post(
            login_url, json={"email": "logintest@gmail.com", "password": "password"}
        )
        assert ac.cookies.get("anonym_site_token", "")
        assert ac.cookies.get("anonym_refresh_token", "")
        yield ac


@pytest.fixture(scope="function")
async def async_client_with_mocked_auth():
    async def mock_get_user():
        return User(**USERS[0])

    async with AsyncClient(
        transport=ASGITransport(app=FastApi_app), base_url="http://test"
    ) as ac:
        FastApi_app.dependency_overrides[get_current_user] = mock_get_user
        yield ac
        FastApi_app.dependency_overrides[mock_get_user] = get_current_user

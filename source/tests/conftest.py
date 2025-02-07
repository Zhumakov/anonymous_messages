"""This module contains prepared fixture for functional test for async requests."""

import json

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy import Insert
from sqlalchemy.ext.asyncio import AsyncSession

from source.auth.models import User
from source.database_service.Base import Base
from source.database_service.database_config import async_engine, session_maker
from source.main import app as FastApi_app
from source.messages.models import Message
from source.settings import settings


def open_json_mock(model: str):
    with open(f"source/tests/mock_{model}.json") as file:
        return json.load(file)


users = open_json_mock("user")
messages = open_json_mock("message")


@pytest.fixture(scope="session")
async def async_client():
    async with AsyncClient(transport=ASGITransport(app=FastApi_app), base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="module", autouse=True)
async def init_database():
    assert settings.MODE == "TEST"

    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with session_maker() as session:
        session: AsyncSession
        add_users = Insert(User).values(users)
        add_messages = Insert(Message).values(messages)

        await session.execute(add_users)
        await session.execute(add_messages)

        await session.commit()


@pytest.fixture(scope="function")
async def auth_async_client():
    async with AsyncClient(transport=ASGITransport(app=FastApi_app), base_url="http://test") as ac:
        await ac.post("/users/auth", json={"email": "logintest@gmail.com", "password": "password"})
        assert ac.cookies.get("anonym_site_token", "")
        assert ac.cookies.get("anonym_refresh_token", "")
        yield ac

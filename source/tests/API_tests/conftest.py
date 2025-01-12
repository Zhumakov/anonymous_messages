"""This module contains prepared fixture for functional test for async requests."""

import pytest
from httpx import ASGITransport, AsyncClient
from source.main import app as FastApi_app


@pytest.fixture(scope="session")
async def async_client():
    async with AsyncClient(
        transport=ASGITransport(app=FastApi_app), base_url="http://test"
    ) as ac:
        yield ac

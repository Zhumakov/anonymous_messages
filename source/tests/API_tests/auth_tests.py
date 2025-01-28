import pytest
from fastapi import status
from httpx import AsyncClient, Response

from source.auth.service import UsersService


@pytest.mark.parametrize(
    "username,email,password,status_code",
    [
        ("User1", "test@gmail.com", "password", status.HTTP_201_CREATED),
        ("User2", "test@gmail.com", "password", status.HTTP_409_CONFLICT),
        ("User1", "test2@gmail.com", "password", status.HTTP_409_CONFLICT),
        ("User4", "test", "password", status.HTTP_422_UNPROCESSABLE_ENTITY),
        ("User5", "test@gmail.com", "", status.HTTP_422_UNPROCESSABLE_ENTITY),
    ],
)
async def test_registration(
    username: str, email: str, password: str, status_code, async_client: AsyncClient
):
    response: Response = await async_client.post(
        "/users", json={"username": username, "email": email, "password": password}
    )

    assert response.status_code == status_code


@pytest.mark.parametrize(
    "email,password,status_code",
    [
        ("logintest@gmail.com", "password", status.HTTP_200_OK),
        ("1234@gmail.com", "password", status.HTTP_401_UNAUTHORIZED),
    ],
)
async def test_login(email: str, password, status_code, async_client: AsyncClient):
    response: Response = await async_client.post(
        "/users/auth", json={"email": email, "password": password}
    )
    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        assert response.cookies.get("anonym_site_token", "")
        assert response.cookies.get("anonym_refresh_token", "")


async def test_logout(auth_async_client: AsyncClient):
    await auth_async_client.delete("/users/auth")
    user = await UsersService.get_by_id(1)
    assert not str(user.refresh_token_id)
    assert not auth_async_client.cookies.get("anonym_site_token", "")
    assert not auth_async_client.cookies.get("anonym_refresh_token", "")


async def test_get_current_user(auth_async_client: AsyncClient):
    response: Response = await auth_async_client.get("/users")
    user = response.json()
    assert user == {"email": "logintest@gmail.com", "username": "logintest"}


async def test_refresh_tokens(auth_async_client: AsyncClient):
    previous_token = auth_async_client.cookies.get("anonym_refresh_token")
    response: Response = await auth_async_client.get("/users/auth/refresh")
    new_token = response.cookies.get("anonym_refresh_token")

    assert previous_token != new_token

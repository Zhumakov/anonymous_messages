import pytest
from fastapi import HTTPException, status
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
    user: dict = response.json()
    plained_user = {"email": "logintest@gmail.com", "user_uid": "1", "username": "logintest"}
    assert all(item in user.items() for item in plained_user.items())


async def test_refresh_tokens(auth_async_client: AsyncClient):
    previous_token = auth_async_client.cookies.get("anonym_refresh_token")
    response: Response = await auth_async_client.get("/users/auth/refresh")
    new_token = response.cookies.get("anonym_refresh_token")

    assert previous_token != new_token


async def test_switch_passwords(async_client: AsyncClient):
    await async_client.post(
        "/users", json={"username": "switch", "email": "email@gmail.com", "password": "password"}
    )
    response: Response = await async_client.post(
        "/users/auth", json={"email": "email@gmail.com", "password": "password"}
    )
    session_token = response.cookies["anonym_site_token"]

    response: Response = await async_client.patch(
        "/users",
        json={"current_password": "password", "new_password": "new_password"},
        cookies={"anonym_site_token": session_token},
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT
    try:
        await UsersService.authenticate_user(email="email@gmail.com", password="password")
        assert False  # Fail
    except HTTPException as exc:
        assert exc.status_code == status.HTTP_401_UNAUTHORIZED

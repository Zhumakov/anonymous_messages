import pytest
from fastapi import status
from httpx import AsyncClient, Response

from source.auth.service import UsersService
from source.main import app


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
    url = app.url_path_for("register_user")
    response: Response = await async_client.post(
        url, json={"username": username, "email": email, "password": password}
    )

    assert response.status_code == status_code


@pytest.mark.parametrize(
    "email,password,status_code",
    [
        ("logintest@gmail.com", "password", status.HTTP_200_OK),
        ("1234@gmail.com", "password", status.HTTP_401_UNAUTHORIZED),
        ("logintest@gmail.com", "wrong_password", status.HTTP_422_UNPROCESSABLE_ENTITY),
    ],
)
async def test_login(email: str, password, status_code, async_client: AsyncClient):
    url = app.url_path_for("login_user")
    response: Response = await async_client.post(url, json={"email": email, "password": password})
    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        assert response.cookies.get("anonym_site_token", "")
        assert response.cookies.get("anonym_refresh_token", "")


async def test_logout(auth_async_client: AsyncClient):
    url = app.url_path_for("logout_user")
    await auth_async_client.delete(url)
    user = await UsersService.get_by_id(1)
    assert not str(user.refresh_token_id)
    assert not auth_async_client.cookies.get("anonym_site_token", "")
    assert not auth_async_client.cookies.get("anonym_refresh_token", "")


async def test_get_current_user(auth_async_client: AsyncClient):
    url = app.url_path_for("get_auth_user")
    response: Response = await auth_async_client.get(url)
    user: dict = response.json()
    plained_user = {"email": "logintest@gmail.com", "user_uid": "1", "username": "logintest"}
    assert all(item in user.items() for item in plained_user.items())


async def test_refresh_tokens(auth_async_client: AsyncClient):
    url = app.url_path_for("refresh_tokens")
    previous_token = auth_async_client.cookies.get("anonym_refresh_token")
    response: Response = await auth_async_client.get(url)
    new_token = response.cookies.get("anonym_refresh_token")

    assert previous_token != new_token


async def test_switch_passwords(async_client: AsyncClient):
    register_url = app.url_path_for("register_user")
    await async_client.post(
        register_url,
        json={"username": "switch", "email": "email@gmail.com", "password": "password"},
    )
    login_url = app.url_path_for("login_user")
    response: Response = await async_client.post(
        login_url, json={"email": "email@gmail.com", "password": "password"}
    )

    switch_pass_url = app.url_path_for("switch_password_current_user")
    response: Response = await async_client.patch(
        switch_pass_url,
        json={"current_password": "password", "new_password": "new_password"},
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT
    response: Response = await async_client.post(
        login_url, json={"email": "email@gmail.com", "password": "password"}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

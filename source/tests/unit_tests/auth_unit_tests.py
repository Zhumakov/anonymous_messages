from typing import Optional

import pytest
from fastapi import HTTPException
from jose import jwt
from sqlalchemy.exc import IntegrityError

from source.auth.core import create_refresh_token, create_session_token
from source.auth.service import UsersService
from source.auth.utils import hash_password, verify_password
from source.exceptions.auth_exc import exceptions
from source.settings import settings


class TestsService:

    @staticmethod
    @pytest.mark.parametrize(
        "username,user_uid,email,password,is_error",
        [
            ("user1", "10", "test@email.com", "password", False),
            ("user1", "11", "test2@email.com", "password", True),
            ("user2", "12", "test@email.com", "password", True),
            ("user3", "10", "test@email.com", "password", True),
        ],
    )
    async def test_create_user(username, user_uid, email, password, is_error):
        try:
            await UsersService.insert_into_table(
                username=username,
                email=email,
                hashed_password=password,
                user_uid=user_uid,
            )
            assert not is_error
        except IntegrityError:
            assert is_error

    @staticmethod
    @pytest.mark.parametrize(
        "token_id,user_id,error",
        (
            ("2523452", 1, None),
            ("2523452", 235245, exceptions.RefreshTokenCreateFailed),
        ),
    )
    async def test_set_refresh_token_id(token_id: str, user_id: int, error: Optional[HTTPException]):
        try:
            await UsersService.set_refresh_token_id(token_id=token_id, user_id=user_id)
            assert not error
        except HTTPException as exc:
            assert exc == error

    @staticmethod
    @pytest.mark.parametrize(
        "email,password,error",
        (
            ("logintest@gmail.com", "password", None),
            ("logintest1234@gmail.com", "password", exceptions.AuthFailed),
            ("logintest@gmail.com", "1234qwer", exceptions.AuthFailed),
        ),
    )
    async def test_authenticate_user(
        email: str, password: str, error: Optional[HTTPException]
    ):
        try:
            assert await UsersService.authenticate_user(email=email, password=password)
            assert not error
        except HTTPException as exc:
            assert exc == error

    @staticmethod
    @pytest.mark.parametrize(
        "current_password,new_password,error",
        (("password", "new_password", None), ("wrong_password", "new_password", exceptions.AuthFailed)),
    )
    async def test_switch_passwords(
        current_password: str, new_password: str, error: Optional[HTTPException]
    ):
        user_email = "logintest@gmail.com"
        try:
            await UsersService.switch_password(
                current_password, new_password, user_email
            )
            assert not error
        except HTTPException as exc:
            assert exc == error


class TestsUtils:

    @staticmethod
    @pytest.mark.parametrize("password", ("pass", "1423", "22_@dsh"))
    async def test_hash_password(password: str):
        hashed_password = hash_password(password)
        assert password != hashed_password

    @staticmethod
    @pytest.mark.parametrize("password", ("pass", "1423", "22_@dsh"))
    async def test_verify_password(password: str):
        hashed_password = hash_password(password)
        assert verify_password(password, hashed_password)


class TestsAuth:

    @staticmethod
    async def test_create_session_token():
        user_id = "1"
        session_token = await create_session_token(user_id)

        user_id_from_token = jwt.decode(
            session_token, settings.SECRET_KEY, settings.ALGORITHM
        ).get("sub")
        assert user_id == user_id_from_token

    @staticmethod
    async def test_create_refresh_token():
        user_id = "1"
        refresh_token = await create_refresh_token(user_id)

        user = await UsersService.get_one_or_none(id=int(user_id))
        assert user

        token_id_from_table = user.refresh_token_id
        token_id_from_token = jwt.decode(
            refresh_token, settings.SECRET_KEY, settings.ALGORITHM
        ).get("token_id")
        assert token_id_from_table == token_id_from_token

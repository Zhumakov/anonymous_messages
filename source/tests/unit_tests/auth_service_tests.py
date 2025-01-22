from typing import Any

import pytest
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from source.auth.auth import create_refresh_token, create_session_token
from source.auth.service import UsersService
from source.auth.utils import hash_password, verify_password
from source.settings import settings


class TestsService:

    @staticmethod
    @pytest.mark.parametrize(
        "username,email,password,result",
        [
            ("user1", "test@email.com", "password", True),
            ("user1", "test2@email.com", "password", False),
            ("user2", "test@email.com", "password", False),
        ],
    )
    async def test_create_user(username, email, password, result):
        query_reslut: Any[bool, ValidationError, IntegrityError] = result

        try:
            query_reslut = await UsersService.insert_into_table(
                username=username, email=email, hashed_password=password
            )
        except (ValidationError, IntegrityError) as exc:
            query_reslut = exc
        finally:
            assert query_reslut == result


class TestsUtils:

    @staticmethod
    @pytest.mark.parametrize("password", ["pass", "1423", "22_@dsh"])
    async def test_hash_password(password: str):
        hashed_password = hash_password(password)
        assert password != hashed_password

    @staticmethod
    @pytest.mark.parametrize("password", ["pass", "1423", "22_@dsh"])
    async def test_verify_password(password: str):
        hashed_password = hash_password(password)
        assert verify_password(password, hashed_password)


class TestsAuth:

    @staticmethod
    async def test_create_session_token():
        user_id = "1"
        session_token = await create_session_token(user_id)

        user_id_from_token = jwt.decode(session_token, settings.SECRET_KEY, settings.ALGORITHM).get(
            "sub"
        )
        assert user_id == user_id_from_token

    @staticmethod
    async def test_create_refresh_token():
        user_id = "1"
        refresh_token = await create_refresh_token(user_id)

        user = await UsersService.get_one_or_none(id=user_id)
        assert user

        token_id_from_table = user.refresh_token_id
        token_id_from_token = jwt.decode(
            refresh_token, settings.SECRET_KEY, settings.ALGORITHM
        ).get("token_id")
        assert token_id_from_table == token_id_from_token

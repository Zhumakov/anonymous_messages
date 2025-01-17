from typing import Any

from pydantic import ValidationError
import pytest
from sqlalchemy.exc import IntegrityError

from source.auth.service import UsersService


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

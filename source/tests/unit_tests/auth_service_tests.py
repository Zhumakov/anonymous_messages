from typing import Any

from pydantic import ValidationError
import pytest

from source.auth.service import UsersService


@pytest.mark.parametrize(
    "email,password,result",
    [
        ("test@email.com", "password", True),
        ("test@email.com", "", ValidationError),
        ("", "password", ValidationError),
        ("test", "password", ValidationError),
    ],
)
async def test_create_user(email, password, result):
    query_reslut: Any[bool, ValidationError] = result

    try:
        user_data = {"email": email, "password": password}
        query_reslut = await UsersService.insert_into_table(data=user_data)
    except ValidationError:
        query_reslut = ValidationError
    finally:
        assert query_reslut == result

import pytest

from source.auth.service import UsersService


@pytest.mark.parametrize(
    "email,password,result",
    [
        ("test@email.com", "password", True),
        ("test@email.com", "", False),
        ("", "password", False),
        ("test", "password", False),
    ],
)
async def test_create_user(email, password, result):
    user_data = {"email": email, "hashed_password": password}
    query_reslut: bool = await UsersService.insert_into_table(data=user_data)
    assert query_reslut == result

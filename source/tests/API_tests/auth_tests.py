import pytest
from fastapi import status
from httpx import AsyncClient, Response


@pytest.mark.parametrize(
    "email,password,status_code",
    [
        ("test@gmail.com", "example", status.HTTP_200_OK),
        ("test", "pass", status.HTTP_422_UNPROCESSABLE_ENTITY),
        ("test@gmail.com", "", status.HTTP_422_UNPROCESSABLE_ENTITY),
    ],
)
async def test_autorization(email, password, status_code, async_client: AsyncClient):
    response: Response = await async_client.post(
        "/users", data={"email": email, "password": password}
    )

    assert response.status_code == status_code

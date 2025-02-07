import pytest
from httpx import AsyncClient, Response


async def test_send_message(async_client_with_mocked_auth: AsyncClient):
    response: Response = await async_client_with_mocked_auth.post(
        "/message", json={"to_user_uid": "2", "body": "test_send_message"}
    )
    assert response.status_code == 201


async def test_reply_on_message(async_client_with_mocked_auth: AsyncClient):
    response: Response = await async_client_with_mocked_auth.post(
        "/message/accepted/3", json={"body": "test_reply_message"}
    )
    assert response.status_code == 201


@pytest.mark.parametrize(
    "category,message_body",
    (("accepted", "message 3"), ("reply", "message 2"), ("sended", "message 1")),
)
async def test_get_messages(
    category: str, message_body: str, async_client_with_mocked_auth: AsyncClient
):
    response: Response = await async_client_with_mocked_auth.get(f"/message/{category}")
    assert response.json()[0].get("body") == message_body

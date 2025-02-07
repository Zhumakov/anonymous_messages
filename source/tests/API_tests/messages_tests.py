import pytest
from httpx import AsyncClient, Response


async def test_send_message(auth_async_client: AsyncClient):
    response: Response = await auth_async_client.post(
        "/message", json={"to_user_uid": "2", "body": "test_send_message"}
    )
    assert response.status_code == 201


async def test_reply_on_message(auth_async_client: AsyncClient):
    response: Response = await auth_async_client.post(
        "/message/accepted?message_id=3", json={"body": "test_reply_message"}
    )
    assert response.status_code == 201


@pytest.mark.parametrize(
    "category,message_body",
    (("accepted", "message 3"), ("reply", "message 2"), ("sended", "message 1")),
)
async def test_get_messages(category: str, message_body: str, auth_async_client: AsyncClient):
    response: Response = await auth_async_client.get(f"/message/{category}")
    assert response.json().get("body") == message_body

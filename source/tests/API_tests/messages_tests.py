import pytest
from httpx import AsyncClient, Response


@pytest.mark.parametrize("to_user_uid,is_error", (("2", False), ("1", True), ("999", True)))
async def test_send_message(
    to_user_uid: str, is_error: bool, async_client_with_mocked_auth: AsyncClient
):
    response: Response = await async_client_with_mocked_auth.post(
        "/message", json={"to_user_uid": to_user_uid, "body": "test_send_message"}
    )
    if not is_error:
        assert response.is_success
    else:
        assert response.is_error


@pytest.mark.parametrize("message_id,is_error", ((3, False), (1, True), (999, True)))
async def test_reply_on_message(
    message_id: int, is_error: bool, async_client_with_mocked_auth: AsyncClient
):
    response: Response = await async_client_with_mocked_auth.post(
        f"/message/accepted/{message_id}", json={"body": "test_reply_message"}
    )
    if not is_error:
        assert response.is_success
    else:
        assert response.is_error


@pytest.mark.parametrize(
    "category,message_body",
    (("accepted", "message 3"), ("reply", "message 2"), ("sended", "message 1")),
)
async def test_get_messages(
    category: str, message_body: str, async_client_with_mocked_auth: AsyncClient
):
    response: Response = await async_client_with_mocked_auth.get(f"/message/{category}")
    assert response.json()[0].get("body") == message_body

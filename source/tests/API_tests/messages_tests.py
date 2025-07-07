import pytest
from httpx import AsyncClient, Response

from source.tests.conftest import FIXED_STR_DATETIME


@pytest.mark.parametrize(
    "category,message_body,username,str_sended_date",
    (
        ("accepted", "message 3", "", FIXED_STR_DATETIME),
        ("reply", "message 2", "messagetest", FIXED_STR_DATETIME),
        ("sended", "message 1", "messagetest", FIXED_STR_DATETIME),
    ),
)
async def test_get_messages(
    category: str,
    message_body: str,
    username: str,
    str_sended_date: str,
    async_client_with_mocked_auth: AsyncClient,
):
    response: Response = await async_client_with_mocked_auth.get(
        f"/api/message/{category}"
    )
    assert response.json()[0].get("body") == message_body
    assert response.json()[0].get("sended_date") == str_sended_date

    if category == "reply":
        assert response.json()[0].get("from_user") == username
    elif category == "sended":
        assert response.json()[0].get("to_user") == username


@pytest.mark.parametrize(
    "to_user_uid,is_error", (("2", False), ("1", True), ("999", True))
)
async def test_send_message(
    to_user_uid: str, is_error: bool, async_client_with_mocked_auth: AsyncClient
):
    response: Response = await async_client_with_mocked_auth.post(
        "/api/message", json={"to_user_uid": to_user_uid, "body": "test_send_message"}
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
        f"/api/message/accepted/{message_id}", json={"body": "test_reply_message"}
    )
    if not is_error:
        assert response.is_success
    else:
        assert response.is_error

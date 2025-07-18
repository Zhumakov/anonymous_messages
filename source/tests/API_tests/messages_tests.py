from typing import Optional
from zoneinfo import ZoneInfo

import pytest
from httpx import AsyncClient, Response


from source.tests.conftest import FIXED_DATETIME
from source.messages.router import DATETIME_FORMAT


@pytest.mark.parametrize(
    "category,message_body,username,time_zone,status_code",
    (
        ("accepted", "message 3", "", "Europe/Warsaw", 200),
        ("accepted", "message 3", "", None, 200),
        ("accepted", "message 3", "", "invalid", 422),
        
        ("reply", "message 2", "messagetest", "Europe/Warsaw", 200),
        ("reply", "message 2", "messagetest", None, 200),
        ("reply", "message 2", "messagetest", "invalid", 422),
        
        ("sended", "message 1", "messagetest", "Europe/Warsaw", 200),
        ("sended", "message 1", "messagetest", None, 200),
        ("sended", "message 1", "messagetest", "invalid", 422),
    ),
)
async def test_get_messages(
    category: str,
    message_body: str,
    username: str,
    time_zone: Optional[str],
    status_code: int,
    async_client_with_mocked_auth: AsyncClient,
):
    if time_zone:
        headers = {"Timezone": time_zone}
    # Default time zone
    else:
        time_zone = "Europe/Moscow"
        headers = {}
        
    response: Response = await async_client_with_mocked_auth.get(
        f"/api/message/{category}", headers=headers
    )
    if status_code != 200:
        assert response.status_code == status_code
    else:
        assert response.json()[0].get("body") == message_body
        assert response.json()[0].get("sended_date") == FIXED_DATETIME.astimezone(ZoneInfo(time_zone)).strftime(DATETIME_FORMAT)

        if category == "reply":
            assert response.json()[0].get("from_user") == username
        elif category == "sended":
            assert response.json()[0].get("to_user") == username


@pytest.mark.parametrize("to_user_uid,is_error", (("2", False), ("1", True), ("999", True)))
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

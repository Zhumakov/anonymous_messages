from datetime import datetime
from typing import Optional

import pytest
from fastapi import HTTPException

from source.exceptions.messages_exc import exceptions
from source.messages.core import (
    get_messsages_on_category,
    send_message,
    verify_and_get_message,
)
from source.messages.service import MessagesService
from source.tests.conftest import FIXED_DATETIME


class TestsService:
    @staticmethod
    @pytest.mark.parametrize(
        "user_uid,plain_result,from_user,sended_date",
        (
            ("1", "message 2", "messagetest", FIXED_DATETIME),
            ("2", "", "", FIXED_DATETIME),
        ),
    )
    async def test_get_replyes(
        user_uid: str, plain_result: str, from_user: str, sended_date: datetime
    ):
        result = await MessagesService.get_replyes(user_uid)
        if plain_result:
            assert str(result[0].body) == plain_result
            assert result[0].sended_date == sended_date
            assert result[0].from_user.username == from_user
        else:
            assert not result

    @staticmethod
    @pytest.mark.parametrize(
        "user_uid,plain_result,sended_date",
        (("1", "message 3", FIXED_DATETIME), ("9999", "", FIXED_DATETIME)),
    )
    async def test_get_accepted(
        user_uid: str, plain_result: str, sended_date: datetime
    ):
        result = await MessagesService.get_accepted(user_uid)
        if plain_result:
            assert str(result[0].body) == plain_result
            assert result[0].sended_date == sended_date
        else:
            assert not result

    @staticmethod
    @pytest.mark.parametrize(
        "user_uid,plain_result,to_user,sended_date",
        (
            ("1", "message 1", "messagetest", FIXED_DATETIME),
            ("9999", "", "", FIXED_DATETIME),
        ),
    )
    async def test_get_sended(
        user_uid: str, plain_result: str, to_user: str, sended_date: datetime
    ):
        result = await MessagesService.get_sended(user_uid)
        if plain_result:
            assert str(result[0].body) == plain_result
            assert result[0].sended_date == sended_date
            assert result[0].to_user.username == to_user
        else:
            assert not result


class TestsCore:
    @staticmethod
    @pytest.mark.parametrize(
        "user_uid,message_id,error",
        (
            ("2", 1, None),
            ("2", 3, exceptions.UserNotAcceptedThisMessage),
            ("2", 9999, exceptions.UserNotAcceptedThisMessage),
            ("2", 2, exceptions.UserNotAcceptedThisMessage),
        ),
    )
    async def test_verify_and_get_message(
        user_uid: str, message_id: int, error: Optional[HTTPException]
    ):
        """
        Test 1: The user received the specified message
        Test 2: The user is trying to reply to a message that is a reply
        Test 3: The specified message does not exist
        Test 4: The specified message was received by another user
        """
        try:
            await verify_and_get_message(user_uid, message_id)
            assert not error
        except HTTPException as exc:
            assert exc == error

    @staticmethod
    @pytest.mark.parametrize(
        "to_user_uid,from_user_uid,error",
        (("2", "1", None), ("2", "2", exceptions.MessageHasNotSended)),
    )
    async def test_send_message(
        to_user_uid: str, from_user_uid: str, error: Optional[HTTPException]
    ):
        try:
            await send_message(
                to_user_uid=to_user_uid,
                from_user_uid=from_user_uid,
                body="Test message",
            )
            assert not error
        except HTTPException as exc:
            assert exc == error

    @staticmethod
    @pytest.mark.parametrize("category,is_exc", (("accepted", False), ("uknown", True)))
    async def test_get_messages_on_cateory(category: str, is_exc: bool):
        try:
            await get_messsages_on_category(category=category, user_uid="1")
            assert not is_exc
        except ValueError:
            assert is_exc

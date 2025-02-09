from typing import Literal, Optional

from sqlalchemy.exc import IntegrityError

from source.exceptions.messages_exc.exceptions import MessageCreateException, MessageVerifyException
from source.messages.models import Message
from source.messages.service import MessagesService


async def verify_and_get_message(from_user_uid: str, reply_to_message: int) -> Message:
    primary_message = await MessagesService.get_by_id(reply_to_message)
    if not primary_message or from_user_uid != primary_message.to_user_uid:
        raise MessageVerifyException("User has not received this message")
    return primary_message


async def send_message_and_notification(
    to_user_uid: str, from_user_uid: str, body: str, reply_to_message: Optional[int] = None
):
    try:
        await MessagesService.insert_into_table(
            to_user_uid=to_user_uid,
            from_user_uid=from_user_uid,
            body=body,
            reply_to_message=reply_to_message,
        )
    except IntegrityError:
        raise MessageCreateException("Couldn't send message")


async def get_messsages_on_category(
    category: Literal["sended", "accepted", "reply"], user_uid: str
):
    match category:
        case "sended":
            results = await MessagesService.get_all(from_user_uid=user_uid)
        case "accepted":
            results = await MessagesService.get_accepted(user_uid=user_uid)
        case "reply":
            results = await MessagesService.get_replyes(user_uid=user_uid)
        case _:
            raise ValueError("Unknown category")

    return tuple(results)

import logging
from datetime import UTC, datetime
from typing import Literal, Optional

from sqlalchemy.exc import IntegrityError

from source.exceptions.messages_exc import exceptions
from source.messages.models import Message
from source.messages.service import MessagesService

logger = logging.getLogger("message_logger")

async def verify_and_get_message(user_uid: str, reply_to_message: int) -> Message:
    """
    Verifies that the specified user has sent the specified message
    Args:
        user_uid (str): The user who was supposed to receive the message
        reply_to_message (int): Message id

    Returns:
        The message received by the user
    """
    primary_message = await MessagesService.get_by_id(reply_to_message)
    # If the user did not receive the message,
    # if it is a reply,
    # if the message was sent by the same user
    if (
        not primary_message
        or bool(primary_message.reply_to_message)
        or user_uid != primary_message.to_user_uid
    ):
        logger.debug("UserNotAcceptedThisMessage: user is not receive this message or it`s reply", extra={"user_uid": user_uid, "reply_to_message": reply_to_message})
        raise exceptions.UserNotAcceptedThisMessage
    return primary_message


async def send_message(
    to_user_uid: str,
    from_user_uid: str,
    body: str,
    reply_to_message: Optional[int] = None,
):
    if to_user_uid == from_user_uid:
        logger.debug("MessageHasNotSended: can't send a message to yourself", extra={"to_user_uid": to_user_uid, "from_user_uid": from_user_uid})
        raise exceptions.MessageHasNotSended
    try:
        await MessagesService.insert_into_table(
            to_user_uid=to_user_uid,
            from_user_uid=from_user_uid,
            body=body,
            reply_to_message=reply_to_message,
            sended_date = datetime.now(UTC)
        )
    except IntegrityError:
        logger.debug("MessageHasNotSended: database error", extra={"to_user_uid": to_user_uid, "from_user_uid": from_user_uid})
        raise exceptions.MessageHasNotSended


async def get_messsages_on_category(
    category: Literal["sended", "accepted", "reply"], user_uid: str
):
    match category:
        case "sended":
            results = await MessagesService.get_sended(user_uid=user_uid)
        case "accepted":
            results = await MessagesService.get_accepted(user_uid=user_uid)
        case "reply":
            results = await MessagesService.get_replyes(user_uid=user_uid)
        case _:
            raise ValueError("Unknown category")

    return tuple(results)

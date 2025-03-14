from fastapi import APIRouter, Depends, status

from source.auth.dependenties import get_current_user
from source.auth.models import User
from source.messages.core import (
    get_messsages_on_category,
    send_message_and_notification,
    verify_and_get_message,
)
from source.messages.schemas import (
    SAcceptedMessageView,
    SReplyMessageView,
    SReplyToMessageRequest,
    SSendedMessageView,
    SSendMessageRequest,
)

router = APIRouter(prefix="/message", tags=["Messages"])


@router.post(
    path="",
    description="sending a message to the specified user",
    status_code=status.HTTP_201_CREATED,
    name="send_message_to_user",
)
async def send_message_to_user(
    message_data: SSendMessageRequest, user: User = Depends(get_current_user)
):
    await send_message_and_notification(
        to_user_uid=message_data.to_user_uid,
        from_user_uid=str(user.user_uid),
        body=message_data.body,
    )
    return {"detail": "The message has been sent"}


@router.post(
    path="/accepted/{message_id}",
    description="Reply to a message with the specified id",
    status_code=status.HTTP_201_CREATED,
    name="reply_on_message",
)
async def reply_on_message(
    message_id: int, message_data: SReplyToMessageRequest, user: User = Depends(get_current_user)
):
    primary_message = await verify_and_get_message(
        user_uid=str(user.user_uid), reply_to_message=message_id
    )
    await send_message_and_notification(
        to_user_uid=str(primary_message.from_user_uid),
        from_user_uid=str(user.user_uid),
        body=message_data.body,
        reply_to_message=message_id,
    )
    return {"detail": "A reply to the message has been sent"}


@router.get(
    path="/sended",
    description="Retrieves a list of sended messages",
    response_model=list[SSendedMessageView],
    name="get_sended_messages",
)
async def get_sended_messages(user: User = Depends(get_current_user)):
    messages = await get_messsages_on_category("sended", str(user.user_uid))
    return messages


@router.get(
    path="/accepted",
    description="Retrieves a list of accepted messages",
    response_model=list[SAcceptedMessageView],
    name="get_accepted_messages",
)
async def get_accepted_messages(user: User = Depends(get_current_user)):
    messages = await get_messsages_on_category("accepted", str(user.user_uid))
    return messages


@router.get(
    path="/reply",
    description="Retrieves a list of reply messages",
    response_model=list[SReplyMessageView],
    name="get_reply_messages",
)
async def get_reply_messages(user: User = Depends(get_current_user)):
    messages = await get_messsages_on_category("reply", str(user.user_uid))
    return messages

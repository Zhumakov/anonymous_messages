from typing import Literal

from fastapi import APIRouter, status

from source.messages.schemas import SAcceptedMessageView, SSendedMessageView

router = APIRouter(prefix="/messages", tags=["Messages"])


@router.post(
    path="/{user_uid}",
    description="sending a message to the specified user",
    status_code=status.HTTP_201_CREATED,
)
async def send_message(user_uid: str):
    pass


@router.post(
    path="/accepted/{message_id}",
    description="Reply to a message with the specified id",
    status_code=status.HTTP_201_CREATED,
)
async def reply_to_message(message_id: int):
    pass


@router.get(
    path="/{category}",
    description="Retrieves a list of messages to the specified category",
    response_model=SAcceptedMessageView | SSendedMessageView,
)
async def get_messages(category: Literal["sended", "accepted", "reply"]):
    pass

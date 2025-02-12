from fastapi import Request, status
from fastapi.responses import JSONResponse

from source.exceptions.messages_exc import exceptions


async def message_verify_exc_handler(request: Request, exc: exceptions.MessageVerifyException):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": "You have not received this message"},
    )


async def message_create_exc_handler(request: Request, exc: exceptions.MessageCreateException):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Couldn't send message"},
    )


async def not_sent_message_to_yourself_exc_handler(
    request: Request, exc: exceptions.NotSentMessageToMyselfException
):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={"detail": "You can't send the message yourself"},
    )

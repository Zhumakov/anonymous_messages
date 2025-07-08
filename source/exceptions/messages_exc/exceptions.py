from fastapi import HTTPException, status



UserNotAcceptedThisMessage = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="The user has not accepted this message",
)

MessageHasNotSended = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Fail to send a message"
)


IncorrectTimeZone = HTTPException(
    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Incorrect timezone"
)

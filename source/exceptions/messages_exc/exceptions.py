from fastapi import HTTPException, status


class MessagesException(Exception):
    def __init__(self, detail: str, *args: object) -> None:
        super().__init__(*args)
        self.detail = detail

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.detail})"


UserNotAcceptedThisMessage = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="The user has not accepted this message",
)

MessageHasNotSended = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Fail to send a message"
)

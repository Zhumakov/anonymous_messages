class MessagesException(Exception):
    def __init__(self, detail: str, *args: object) -> None:
        super().__init__(*args)
        self.detail = detail

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.detail})"


class MessageVerifyException(MessagesException):
    pass


class MessageCreateException(MessagesException):
    pass


class NotSentMessageToMyselfException(MessagesException):
    pass

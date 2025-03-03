class AuthException(Exception):
    def __init__(self, detail: str, *args: object) -> None:
        super().__init__(*args)
        self.detail = detail

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({self.detail})"


class IsNotAuthorized(AuthException):
    pass


class UserCreateException(AuthException):
    pass


class TokenValidException(AuthException):
    pass


class TokenDataException(AuthException):
    pass


class UserIsNotExistException(AuthException):
    pass


class RefreshTokenIdIsNotValidException(AuthException):
    pass


class RefreshTokenSetException(AuthException):
    pass


class PasswordIsInvalidException(AuthException):
    pass


class PasswordChangeException(AuthException):
    pass


class ExistingUserException(AuthException):
    pass


class ExistingUsernameException(AuthException):
    pass

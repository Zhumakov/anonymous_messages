from fastapi import Request, status
from fastapi.responses import JSONResponse

from source.exceptions.auth_exc import exceptions


async def user_create_exc_handler(request: Request, exc: exceptions.UserCreateException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Failed to register the user"},
    )


async def is_not_authorized(request: Request, exc: exceptions.IsNotAuthorized):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": "User is not authorized"}
    )


async def exist_user_exc_handler(request: Request, exc: exceptions.ExistingUserException):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": "User with this email is already exist"},
    )


async def exist_username_exc_handler(request: Request, exc: exceptions.ExistingUsernameException):
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={"detail": "User with this username is already exist"},
    )


async def user_is_not_exist_exc_handler(request: Request, exc: exceptions.UserIsNotExistException):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED, content={"detail": "User is not exist"}
    )


async def pass_change_exc_handler(request: Request, exc: exceptions.PasswordChangeException):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Failed to change password"},
    )


async def pass_is_not_valid_exc_handler(
    request: Request, exc: exceptions.PasswordIsInvalidException
):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "Password is not valid"},
    )


async def refresh_token_id_is_not_valid_exc_handler(
    request: Request, exc: exceptions.RefreshTokenIdIsNotValidException
):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN, content={"detail": "Refresh token is not valid"}
    )


async def refresh_token_set_exc_handler(request: Request, exc: exceptions.RefreshTokenSetException):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Failed to create a refresh token"},
    )


async def token_data_exc_hander(request: Request, exc: exceptions.TokenDataException):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": "Token data is not valid"},
    )


async def token_valid_exc_handler(request: Request, exc: exceptions.TokenValidException):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"detail": "Token is not valid"}
    )

from typing import Optional

from fastapi import Cookie
from jose import JWTError, jwt

from source.auth.models import User
from source.auth.service import UsersService
from source.exceptions.auth_exc import exceptions
from source.settings import settings


async def get_current_user(
    anonym_site_token: Optional[str] = Cookie(None, description="Token for autorize"),
) -> User:
    if not anonym_site_token:
        raise exceptions.IsNotAuthorized("Session token is not exist")

    try:
        payload = jwt.decode(
            anonym_site_token, key=settings.SECRET_KEY, algorithms=settings.ALGORITHM
        )
    except JWTError:
        raise exceptions.TokenValidException("Session token is not valid")

    user_id = payload.get("sub")
    if not user_id:
        raise exceptions.TokenDataException("Token data is not valid")

    user = await UsersService.get_by_id(int(user_id))
    if not user:
        raise exceptions.UserIsNotExistException("The user is not exist")

    return user


async def verify_refresh_token(
    anonym_site_refresh: str = Cookie(description="Cookie for refresh tokens"),
) -> User:
    try:
        payload = jwt.decode(
            anonym_site_refresh, key=settings.SECRET_KEY, algorithms=settings.ALGORITHM
        )
    except JWTError:
        raise exceptions.TokenValidException("Refresh token is not valid")

    user: User = await get_current_user(anonym_site_refresh)

    token_id = payload.get("token_id")
    if not token_id:
        raise exceptions.TokenDataException("Token data is not valid")

    if user.refresh_token_id != token_id:
        raise exceptions.RefreshTokenIdIsNotValidException("Refresh token id is not valid")

    return user

from fastapi import Cookie
from jose import JWTError, jwt

from source import exceptions
from source.auth.models import User
from source.auth.service import UsersService
from source.settings import settings


async def get_current_user(
    anonym_site_token: str = Cookie(description="Token for autorize"),
) -> User:
    try:
        payload = jwt.decode(
            anonym_site_token, key=settings.SECRET_KEY, algorithms=settings.ALGORITHM
        )
    except JWTError:
        raise exceptions.TokenValidHTTPException

    user_id = payload.get("sub")
    if not user_id:
        raise exceptions.TokenDataHTTPException

    user = await UsersService._get_by_id(int(user_id))
    if not user:
        raise exceptions.UserIsNotExistHTTPException

    return user


async def verify_refresh_token(
    anonym_site_refresh: str = Cookie(description="Cookie for refresh tokens"),
) -> User:
    try:
        payload = jwt.decode(
            anonym_site_refresh, key=settings.SECRET_KEY, algorithms=settings.ALGORITHM
        )
    except JWTError:
        raise exceptions.TokenValidHTTPException

    user: User = await get_current_user(anonym_site_refresh)

    token_id = payload.get("token_id")
    if not token_id:
        raise exceptions.TokenDataHTTPException

    if user.refresh_token_id != token_id or not str(user.refresh_token_id):
        raise exceptions.RefreshTokenIdIsNotValidHTTPException

    return user

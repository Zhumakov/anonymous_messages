from typing import Optional

from fastapi import Cookie
from jose import JWTError, jwt

from source.auth.service import UsersService
from source.exceptions.auth_exc import exceptions
from source.settings import settings


async def get_current_user(
    anonym_site_token: Optional[str] = Cookie(None, description="Token for autorize")
):
    if not anonym_site_token:
        raise exceptions.IsNotAuthorized

    try:
        payload = jwt.decode(
            anonym_site_token, key=settings.SECRET_KEY, algorithms=settings.ALGORITHM
        )
    except JWTError:
        raise exceptions.TokenValidException

    user_id = payload.get("sub")
    if not user_id:
        raise exceptions.IsNotAuthorized

    user = await UsersService.get_by_id(int(user_id))
    if not user:
        raise exceptions.IsNotAuthorized

    return user

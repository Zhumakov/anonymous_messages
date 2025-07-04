import logging
from typing import Optional

from fastapi import Cookie
from jose import JWTError, jwt

from source.auth.service import UsersService
from source.exceptions.auth_exc import exceptions
from source.settings import settings

logger = logging.getLogger("auth_logger")


async def get_current_user(
    anonym_site_token: Optional[str] = Cookie(None, description="Token for autorize")
):
    if not anonym_site_token:
        logger.debug("IsNotAuthorized: the user does not have a session token")
        raise exceptions.IsNotAuthorized

    try:
        payload = jwt.decode(
            anonym_site_token, key=settings.SECRET_KEY, algorithms=settings.ALGORITHM
        )
    except JWTError:
        logger.debug("TokenValidException: token is invalid")
        raise exceptions.TokenValidException

    user_id = payload.get("sub")
    if not user_id:
        logger.debug("IsNotAuthorized: the token does not gave a user_id")
        raise exceptions.IsNotAuthorized

    user = await UsersService.get_by_id(int(user_id))
    if not user:
        logger.debug("IsNotAuthorized: user is not exist")
        raise exceptions.IsNotAuthorized

    return user

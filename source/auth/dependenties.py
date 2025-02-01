from fastapi import Cookie, Depends, HTTPException, status
from jose import JWTError, jwt

from source.auth.models import Users
from source.auth.service import UsersService
from source.settings import settings


async def get_current_user(
    anonym_site_token: str = Cookie(description="Token for autorize"),
) -> Users:
    try:
        payload = jwt.decode(
            anonym_site_token, key=settings.SECRET_KEY, algorithms=settings.ALGORITHM
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is not valid or he has expire"
        )
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="There is no data of user"
        )

    if not (user := await UsersService.get_by_id(int(user_id))):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not registred"
        )

    return user


async def verify_refresh_token(
    anonym_site_refresh: str = Cookie(description="Cookie for refresh tokens"),
) -> Users:
    try:
        payload = jwt.decode(
            anonym_site_refresh, key=settings.SECRET_KEY, algorithms=settings.ALGORITHM
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token is not valid or he has expire",
        )

    user: Users = await get_current_user(anonym_site_refresh)

    token_id = payload.get("token_id")
    if not token_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token id is not found"
        )

    if user.refresh_token_id != token_id or not str(user.refresh_token_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Refresh token id is not valid, or the user is logged out",
        )

    return user

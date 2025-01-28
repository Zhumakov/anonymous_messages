from fastapi import Depends, HTTPException, Request, status
from jose import JWTError, jwt

from source.auth.models import Users
from source.auth.service import UsersService
from source.settings import settings


def get_token(request: Request) -> str:
    token = request.cookies.get("anonym_site_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is not found")

    try:
        jwt.decode(token, key=settings.SECRET_KEY, algorithms=settings.ALGORITHM)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is not valid or he has expire"
        )

    return token


def get_refresh_token(request: Request) -> str:
    refresh_token = request.cookies.get("anonym_site_refresh")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token is not found"
        )

    try:
        jwt.decode(refresh_token, key=settings.SECRET_KEY, algorithms=settings.ALGORITHM)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token is not valid or he has expire",
        )

    return refresh_token


async def get_current_user(token: str = Depends(get_token)) -> Users:
    payload = jwt.decode(token, key=settings.SECRET_KEY, algorithms=settings.ALGORITHM)

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="There is no data of user"
        )

    user = await UsersService.get_by_id(int(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not registred"
        )

    return user


async def verify_refresh_token(refresh_token: str) -> bool | Users:
    user: Users = await get_current_user(refresh_token)
    payload = jwt.decode(refresh_token, key=settings.SECRET_KEY, algorithms=settings.ALGORITHM)

    token_id = payload.get("token_id")
    if not token_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Token id is not found"
        )

    if user.refresh_token_id != token_id or not str(user.refresh_token_id):
        return False

    return user

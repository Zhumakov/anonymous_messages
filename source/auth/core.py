import uuid
from datetime import UTC, datetime, timedelta

from fastapi import Response
from jose import JWTError, jwt
from sqlalchemy.exc import IntegrityError

from source.auth.dependenties import get_current_user
from source.auth.models import User
from source.auth.schemas import SUserRegistration
from source.auth.service import UsersService
from source.auth.utils import hash_password, jwt_encode
from source.exceptions.auth_exc import exceptions
from source.settings import settings


async def verify_refresh_token(refresh_token: str) -> User:
    try:
        payload = jwt.decode(
            refresh_token, key=settings.SECRET_KEY, algorithms=settings.ALGORITHM
        )
    except JWTError:
        raise exceptions.TokenValidException

    user: User = await get_current_user(refresh_token)

    token_id = payload.get("token_id")
    if not token_id:
        raise exceptions.RefreshTokenIsInvalid

    if user.refresh_token_id != token_id:
        raise exceptions.RefreshTokenIsInvalid

    return user


async def register_user(user_data: SUserRegistration):
    if await UsersService.get_one_or_none(email=user_data.email):
        raise exceptions.UserAlreadyExist

    if await UsersService.get_one_or_none(username=user_data.username):
        raise exceptions.UsernameAlreadyExist

    hashed_password = hash_password(user_data.password)
    user_uid = str(uuid.uuid4())
    try:
        await UsersService.insert_into_table(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password,
            user_uid=user_uid,
        )
    except IntegrityError:
        raise exceptions.UserCreateFail


async def create_refresh_token(user_id: str) -> str:
    expire = datetime.now(UTC) + timedelta(days=30)

    token_id = str(uuid.uuid4())
    try:
        await UsersService.set_refresh_token_id(token_id=token_id, user_id=int(user_id))
    except IntegrityError:
        raise exceptions.RefreshTokenCreateFailed

    to_encode = {
        "sub": str(user_id),
        "token_id": token_id,
        "exp": expire,
    }

    return jwt_encode(to_encode)


async def create_session_token(user_id: str) -> str:
    expire = datetime.now(UTC) + timedelta(minutes=15)
    to_encode = {"sub": user_id, "exp": expire}
    return jwt_encode(to_encode)


async def set_tokens_in_cookies(
    response: Response, user_id: str
) -> tuple[Response, str, str]:
    session_token = await create_session_token(user_id)
    refresh_token = await create_refresh_token(user_id)
    response.set_cookie("anonym_site_token", session_token)
    response.set_cookie("anonym_refresh_token", refresh_token)

    return response, session_token, refresh_token

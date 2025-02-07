import uuid
from datetime import datetime, timedelta, timezone

from fastapi import Response

from source.auth.schemas import SUserRegistration
from source.auth.service import UsersService
from source.auth.utils import hash_password, jwt_encode


async def register_user(user_data: SUserRegistration):
    hashed_password = hash_password(user_data.password)
    user_uid = str(uuid.uuid4())
    await UsersService.insert_into_table(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        user_uid=user_uid,
    )


async def create_refresh_token(user_id: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(days=30)

    token_id = str(uuid.uuid4())
    await UsersService.set_refresh_token_id(token_id=token_id, user_id=int(user_id))

    to_encode = {
        "sub": str(user_id),
        "token_id": token_id,
        "exp": expire,
    }

    return jwt_encode(to_encode)


async def create_session_token(user_id: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode = {"sub": user_id, "exp": expire}
    return jwt_encode(to_encode)


async def set_tokens_in_cookies(response: Response, user_id: str) -> tuple[Response, str, str]:
    session_token = await create_session_token(user_id)
    refresh_token = await create_refresh_token(user_id)
    response.set_cookie("anonym_site_token", session_token)
    response.set_cookie("anonym_refresh_token", refresh_token)

    return response, session_token, refresh_token

from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import jwt

from source.settings import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_session_token(**kwargs) -> str:
    to_encode = kwargs.copy()
    expire =str(datetime.now(timezone.utc) + timedelta(minutes=15))
    to_encode.update({"expire": expire})
    encoded_jwt = jwt.encode(
        claims=to_encode, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt

from jose import jwt
from passlib.context import CryptContext

from source.settings import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hash_password: str) -> bool:
    return pwd_context.verify(plain_password, hash_password)


def jwt_encode(to_encode):
    return jwt.encode(to_encode, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)

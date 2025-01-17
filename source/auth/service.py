from fastapi import HTTPException, status

from source.auth.models import Users
from source.database_service.Base import BaseService
from source.auth.auth import verify_password


class UsersService(BaseService[Users]):
    model = Users

    @classmethod
    async def authenticate_user(cls, email: str, password: str) -> Users:
        user = await cls.get_one_or_none(email=email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not exist"
            )

        password_is_valid = verify_password(password, user.hashed_password)
        if not password_is_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Password is valid"
            )

        return user

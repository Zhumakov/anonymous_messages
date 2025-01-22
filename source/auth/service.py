from fastapi import HTTPException, status

from source.auth.models import Users
from source.auth.utils import verify_password
from source.database_service.Base import BaseService


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

    @classmethod
    async def set_refresh_token_id(cls, token_id: str, user_id: int) -> bool:
        user = await cls.get_one_or_none(id=user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not exist"
            )

        filter_by = {"id": user_id}
        values = {"refresh_token_id": token_id}
        set_result = await cls.update_node(filter_by, values)
        return set_result

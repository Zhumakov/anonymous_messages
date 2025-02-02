import uuid

from fastapi import HTTPException, status

from source import exceptions
from source.auth.models import Users
from source.auth.schemas import SUserFilterQuery, SUserInsertQuery, SUserUpdateQuery
from source.auth.utils import hash_password, verify_password
from source.database_service.Base import BaseService


class UsersService(BaseService[Users, SUserFilterQuery, SUserInsertQuery, SUserUpdateQuery]):

    model = Users
    filter_model_scheme = SUserFilterQuery
    update_model_scheme = SUserUpdateQuery
    model_node_scheme = SUserInsertQuery

    @classmethod
    async def authenticate_user(cls, email: str, password: str) -> Users:
        user = await cls.get_one_or_none(email=email)
        if not user:
            raise exceptions.UserIsNotExistHTTPException

        password_is_valid = verify_password(password, str(user.hashed_password))
        if not password_is_valid:
            raise exceptions.PasswordIsInvalidHTTPException

        return user

    @classmethod
    async def set_refresh_token_id(cls, token_id: str, user_id: int) -> bool:
        if not await cls.get_by_id(user_id):
            raise exceptions.UserIsNotExistHTTPException

        filter_by = {"id": user_id}
        values = {"refresh_token_id": token_id}
        set_result = await cls.update_node(filter_by, values)
        return set_result

    @classmethod
    async def switch_password(cls, new_password: str, user_id: int):
        if not await cls.get_by_id(user_id):
            raise exceptions.UserIsNotExistHTTPException

        hashed_password = hash_password(new_password)

        filter_by = {"id": user_id}
        values = {"hashed_password": hashed_password}
        set_result = await cls.update_node(filter_by, values)
        return set_result

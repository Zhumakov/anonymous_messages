from source import exceptions
from source.auth.models import User
from source.auth.schemas import SUserFilterQuery, SUserInsertQuery, SUserUpdateQuery
from source.auth.utils import hash_password, verify_password
from source.database_service.Base import BaseService


class UsersService(BaseService[User, SUserFilterQuery, SUserInsertQuery, SUserUpdateQuery]):

    model = User
    filter_model_scheme = SUserFilterQuery
    update_model_scheme = SUserUpdateQuery
    model_node_scheme = SUserInsertQuery

    @classmethod
    async def authenticate_user(cls, email: str, password: str) -> User:
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
    async def switch_password(cls, old_password: str, new_password: str, user_email: str):
        await cls.authenticate_user(user_email, old_password)

        hashed_password = hash_password(new_password)

        filter_by = {"email": user_email}
        values = {"hashed_password": hashed_password}
        set_result = await cls.update_node(filter_by, values)
        return set_result

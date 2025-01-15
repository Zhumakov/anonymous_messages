from source.auth.models import Users
from source.auth.schemas import SUserRequest
from source.database_service.Base import BaseService


class UsersService(BaseService[Users, SUserRequest]):
    model = Users
    pydantic_scheme = SUserRequest

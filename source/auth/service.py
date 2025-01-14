from source.auth.models import Users
from source.database_service.Base import BaseService


class UsersService(BaseService):
    model = Users

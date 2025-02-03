from source.auth.schemas import SUserFilterQuery, SUserInsertQuery, SUserUpdateQuery
from source.database_service.Base import BaseService
from source.messages.models import Message


class MessagesService(BaseService[Message, SUserFilterQuery, SUserInsertQuery, SUserUpdateQuery]):

    model = Message
    filter_model_scheme = SUserFilterQuery
    update_model_scheme = SUserUpdateQuery
    model_node_scheme = SUserInsertQuery


    @classmethod
    async def create_message(cls, to_user_uid: str, from_user_uid: str, body: str, category: )
        pass

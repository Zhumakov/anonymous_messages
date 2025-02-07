from typing import Sequence

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from source.auth.schemas import SUserFilterQuery, SUserInsertQuery, SUserUpdateQuery
from source.database_service.Base import BaseService
from source.messages.models import Message


class MessagesService(BaseService[Message, SUserFilterQuery, SUserInsertQuery, SUserUpdateQuery]):

    model = Message
    filter_model_scheme = SUserFilterQuery
    update_model_scheme = SUserUpdateQuery
    model_node_scheme = SUserInsertQuery

    @classmethod
    async def get_replyes(cls, user_uid) -> Sequence[Message]:
        async with cls.async_session_maker() as session:
            session: AsyncSession
            query = Select(cls.model).filter(
                Message.to_user_uid == user_uid, Message.reply_to_message.is_not(None)
            )
            results = await session.execute(query)
            return results.scalars().all()

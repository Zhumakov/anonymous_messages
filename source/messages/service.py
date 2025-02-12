from typing import Sequence

from sqlalchemy import Select
from sqlalchemy.ext.asyncio import AsyncSession

from source.database_service.Base import BaseService
from source.messages.models import Message
from source.messages.schemas import SMessageFilterQuery, SMessageInsertQuery, SMessageUpdateQuery


class MessagesService(
    BaseService[Message, SMessageFilterQuery, SMessageInsertQuery, SMessageUpdateQuery]
):

    model = Message
    filter_model_scheme = SMessageFilterQuery
    update_model_scheme = SMessageUpdateQuery
    model_node_scheme = SMessageInsertQuery

    @classmethod
    async def get_replyes(cls, user_uid: str) -> Sequence[Message]:
        async with cls.async_session_maker() as session:
            session: AsyncSession
            query = Select(cls.model).filter(
                Message.to_user_uid == user_uid, Message.reply_to_message.is_not(None)
            )
            results = await session.execute(query)
            return results.scalars().all()

    @classmethod
    async def get_accepted(cls, user_uid: str) -> Sequence[Message]:
        async with cls.async_session_maker() as session:
            session: AsyncSession
            query = Select(cls.model).filter(
                Message.to_user_uid == user_uid, Message.reply_to_message.is_(None)
            )
            results = await session.execute(query)
            return results.scalars().all()

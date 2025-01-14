from dataclasses import astuple
from typing import Annotated

from sqlalchemy import Delete, Insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from source.database_service.database_config import session_maker


class BaseService:
    """Class for shared database functions"""

    model = None

    @classmethod
    async def get_by_id(cls, model_id: int):
        async with session_maker() as session:
            session: AsyncSession
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def get_one_or_none(cls, filter_data: dict):
        async with session_maker() as session:
            session: AsyncSession
            query = select(cls.model).filter_by(**filter_data)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def insert_into_table(cls, data: dict):
        async with session_maker() as session:
            session: AsyncSession
            query = Insert(cls.model).values(**data)
            try:
                await session.execute(query)
                await session.commit()
                return True
            except IntegrityError:
                return False

    @classmethod
    async def delete_by_id(cls, id_node: int):
        async with session_maker() as session:
            session: AsyncSession
            query = Delete(cls.model).filter_by(id=id_node)
            await session.execute(query)
            await session.commit()

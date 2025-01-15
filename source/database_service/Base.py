from typing import Generic, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import Delete, Insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from source.database_service.database_config import Base, session_maker


ModelType = TypeVar("ModelType", bound=Base)
PydanticSchemeType = TypeVar("PydanticSchemeType", bound=BaseModel)


class BaseService(Generic[ModelType, PydanticSchemeType]):
    """Class for shared database functions"""

    model: Type[ModelType]
    pydantic_scheme: Type[PydanticSchemeType]

    @classmethod
    async def get_by_id(cls, model_id: int) -> ModelType | None:
        async with session_maker() as session:
            session: AsyncSession
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def get_one_or_none(cls, filter_data: dict) -> ModelType | None:
        async with session_maker() as session:
            session: AsyncSession
            query = select(cls.model).filter_by(**filter_data)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def insert_into_table(cls, data: dict) -> bool:
        user_data = cls.pydantic_scheme(**data)
        async with session_maker() as session:
            session: AsyncSession
            query = Insert(cls.model).values(**user_data.model_dump())
            try:
                await session.execute(query)
                await session.commit()
                return True
            except IntegrityError:
                return False

    @classmethod
    async def delete_by_id(cls, id_node: int) -> None:
        async with session_maker() as session:
            session: AsyncSession
            query = Delete(cls.model).filter_by(id=id_node)
            await session.execute(query)
            await session.commit()

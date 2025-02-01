from typing import Generic, Type, TypeVar

from pydantic import BaseModel, ValidationError
from sqlalchemy import Delete, Insert, select, update
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from source.database_service.database_config import Base, session_maker

ModelType = TypeVar("ModelType", bound=Base)
FilterModelScheme = TypeVar("FilterModelScheme", bound=BaseModel)
UpdateModelScheme = TypeVar("UpdateModelScheme", bound=BaseModel)
ModelNodeScheme = TypeVar("ModelNodeScheme", bound=BaseModel)


class BaseService(Generic[ModelType, FilterModelScheme, ModelNodeScheme, UpdateModelScheme]):
    """Class for shared database functions"""

    model: Type[ModelType]
    filter_model_scheme: Type[FilterModelScheme]
    update_model_scheme: Type[UpdateModelScheme]
    model_node_scheme: Type[ModelNodeScheme]

    @classmethod
    async def get_by_id(cls, model_id: int) -> ModelType | None:
        async with session_maker() as session:
            session: AsyncSession
            query = select(cls.model).filter_by(id=model_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def get_one_or_none(cls, **kwargs) -> ModelType | None:
        cls.filter_model_scheme.model_validate(kwargs)
        if not kwargs:
            raise ValidationError("Input dictionary cannot be empty.", ())

        async with session_maker() as session:
            session: AsyncSession
            query = select(cls.model).filter_by(**kwargs)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def insert_into_table(cls, **kwargs) -> bool:
        cls.model_node_scheme.model_validate(kwargs)

        async with session_maker() as session:
            session: AsyncSession
            query = Insert(cls.model).values(**kwargs)
            await session.execute(query)
            await session.commit()
            return True

    @classmethod
    async def update_node(cls, filter_by: dict, values: dict) -> bool:
        cls.filter_model_scheme.model_validate(filter_by)
        cls.update_model_scheme.model_validate(values)
        if not filter_by or not values:
            raise ValidationError("Input dictionaries cannot be empty.", ())

        async with session_maker() as session:
            session: AsyncSession
            query = update(cls.model).filter_by(**filter_by).values(**values)
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

from typing import Annotated

from fastapi import Depends
from source.database_service.database_config import get_session
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class BaseService:
    """Class for shared database functions"""

    model = None

    @classmethod
    async def get_by_id(
        cls, session: Annotated[AsyncSession, Depends(get_session)], model_id
    ):
        query = select(cls).filter_by(id=model_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()

from pydantic import ConfigDict
from sqlalchemy import Column, Integer, String


from source.database_service.database_config import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)

    model_config = ConfigDict(from_attributes=True)

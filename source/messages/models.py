from enum import Enum as PythonEnum

from pydantic import ConfigDict
from sqlalchemy import Column, Enum, ForeignKey, Integer, String

from source.database_service.database_config import Base


class MessageCategory(PythonEnum):
    SENDED = "sended"
    ACCEPTED = "accepted"
    REPLY = "reply"


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    from_user_uid = Column(Integer, ForeignKey("users.user_uid"))
    to_user_uid = Column(Integer, ForeignKey("users.user_uid"))
    category = Column(Enum(MessageCategory))
    body = Column(String, nullable=False)

    model_config = ConfigDict(from_attributes=True)

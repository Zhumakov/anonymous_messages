from pydantic import ConfigDict
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import Relationship

from source.database_service.database_config import Base


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    from_user_uid = Column(String, ForeignKey("users.user_uid"))
    to_user_uid = Column(String, ForeignKey("users.user_uid"))
    reply_to_message = Column(Integer, nullable=True)
    body = Column(String, nullable=False)

    from_user = Relationship(
        "User", foreign_keys="[Message.from_user_uid]", back_populates="sent_messages"
    )
    to_user = Relationship(
        "User", foreign_keys="[Message.to_user_uid]", back_populates="received_messages"
    )

    model_config = ConfigDict(from_attributes=True)

from pydantic import ConfigDict
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Relationship

from source.database_service.database_config import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)

    # It is used to send messages to the user
    user_uid = Column(String, unique=True, nullable=False)

    username = Column(String, unique=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    hashed_password = Column(String, nullable=False)
    refresh_token_id = Column(String, nullable=True)

    sent_messages = Relationship(
        "Message", foreign_keys="[Message.from_user_uid]", back_populates="from_user"
    )
    received_messages = Relationship(
        "Message", foreign_keys="[Message.to_user_uid]", back_populates="to_user"
    )

    model_config = ConfigDict(from_attributes=True)

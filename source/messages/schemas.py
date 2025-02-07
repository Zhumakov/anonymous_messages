from typing import Optional

from pydantic import BaseModel


class SSendedMessageView(BaseModel):
    """Displaying sent messages"""

    id: int
    to_user_uid: str
    body: str


class SAcceptedMessageView(BaseModel):
    """Displaying accepted messages"""

    id: int
    body: str


class SReplyMessageView(BaseModel):
    """Displaying reply messages"""

    id: int
    from_user_uid: str
    body: str


class SSendMessageRequest(BaseModel):
    "For message sending requests"

    to_user_uid: str
    body: str


class SReplyToMessageRequest(BaseModel):
    "For reply to message requests"

    body: str


class SMessageFilterQuery(BaseModel):
    """Using in the FILTER BY query"""

    id: Optional[int] = None
    from_user_uid: Optional[str] = None
    to_user_uid: Optional[str] = None

    model_config = {"strict": True, "extra": "forbid"}


class SMessageUpdateQuery(BaseModel):
    """Using in the UPDATE query"""

    from_user_uid: Optional[str] = None
    to_user_uid: Optional[str] = None
    body: Optional[str] = None


class SMessageInsertQuery(BaseModel):
    """Using in the INSERT queryes"""

    from_user_uid: str
    to_user_uid: str
    reply_to_message: Optional[int] = None
    body: str

    model_config = {"strict": True, "extra": "forbid"}

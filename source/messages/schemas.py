from typing import Optional

from pydantic import BaseModel


class SSendedMessageView(BaseModel):

    id: int
    to_user_id: str
    body: str


class SAcceptedMessageView(BaseModel):

    id: int
    body: str


class SReplyMessageView(BaseModel):

    id: int
    from_user_id: str
    body: str


class SMessageFilterQuery(BaseModel):
    """Using in the FILTER BY query"""

    id: Optional[int] = None
    from_user_id: Optional[int] = None
    to_user_id: Optional[int] = None

    model_config = {"strict": True, "extra": "forbid"}


class SMessageUpdateQuery(BaseModel):
    """Using in the UPDATE query"""

    from_user_id: Optional[int] = None
    to_user_id: Optional[int] = None
    body: Optional[str] = None


class SMessageInsertQuery(BaseModel):
    """Using in the INSERT queryes"""

    from_user_id: int
    to_user_id: int
    body: str

    model_config = {"strict": True, "extra": "forbid"}

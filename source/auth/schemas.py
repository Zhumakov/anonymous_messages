from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class SUserLogin(BaseModel):
    """Using for login"""

    email: EmailStr
    password: str = Field(..., min_length=4)


class SUserRegistration(BaseModel):
    """Using for registration"""

    username: str
    email: EmailStr
    password: str = Field(..., min_length=4)


class SUserResponse(BaseModel):
    """Using for response"""

    username: str
    email: EmailStr


class SUserSwitchPassword(BaseModel):
    """Using for switch_password"""

    password: str = Field(..., min_length=4)


class SUserFilterQuery(BaseModel):
    """Using in the FILTER BY query"""

    id: Optional[int] = None
    username: Optional[str] = None
    email: Optional[str] = None
    refresh_token_id: Optional[str] = None
    register_token: Optional[str] = None

    model_config = {"strict": True, "extra": "forbid"}


class SUserUpdateQuery(BaseModel):
    """Using in the UPDATE query"""

    username: Optional[str] = None
    email: Optional[EmailStr] = None
    hashed_password: Optional[str] = None
    refresh_token_id: Optional[str] = None
    register_token: Optional[str] = None


class SUserInsertQuery(BaseModel):
    """Using in the INSERT queryes"""

    username: str
    email: EmailStr
    hashed_password: str

    model_config = {"strict": True, "extra": "forbid"}

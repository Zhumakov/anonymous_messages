from typing import Optional

from pydantic import BaseModel, EmailStr, Field, field_validator, validator


class SUserLogin(BaseModel):
    """Using for login"""

    email: EmailStr
    password: str

    @field_validator("password")
    def validate_password(cls, value: str):
        if len(value) < 4:
            raise ValueError("Password must be len >= 4")
        return value


class SUserRegistration(SUserLogin):
    """Using for registration"""

    username: str


class SUserResponse(BaseModel):
    """Using for response"""

    username: str
    email: EmailStr


class SUserFilterQuery(BaseModel):
    """Using in FILTER BY and in UPDATE queryes"""

    id: Optional[int] = None
    username: Optional[str] = None
    email: Optional[str] = None
    hashed_password: Optional[str] = None
    refresh_token_id: Optional[str] = None

    model_config = {"strict": True, "extra": "forbid"}


class SUserInsertQuery(BaseModel):
    """Using in INSERT queryes"""

    username: str
    email: EmailStr
    hashed_password: str

    model_config = {"strict": True, "extra": "forbid"}

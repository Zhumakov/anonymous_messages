from pydantic import BaseModel, EmailStr, field_validator


class SUserLogin(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    def validate_password(cls, value: str):
        if len(value) < 4:
            raise ValueError("Password must be len >= 4")
        return value


class SUserRequest(SUserLogin):
    username: str

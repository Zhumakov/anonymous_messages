from pydantic import BaseModel, EmailStr, field_validator


class SUserRequest(BaseModel):
    email: EmailStr
    password: str

    @field_validator("password")
    def validate_password(cls, vlaue: str):
        if len(vlaue) < 4:
            raise ValueError("Password must be len >= 4")
        return vlaue

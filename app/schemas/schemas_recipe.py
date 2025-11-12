from pydantic import EmailStr, BaseModel, field_validator, model_validator
from uuid import UUID
from typing import Optional


class BaseUser(BaseModel):
    username: str
    email: EmailStr


class CreateUser(BaseUser):
    password: str

    @field_validator("username")
    def capitalize(cls, value):
        return value.title()

    @field_validator("password")
    def length_check(cls, value):
        if len(value) <= 7:
            raise ValueError("the password must be at least 8 symbols long.")

        return value


class User(BaseUser):
    id: UUID


class UpdateUser(BaseModel):
    username: Optional[str] | None = None
    email: Optional[EmailStr] | None = None
    password: Optional[str] | None = None

    @model_validator(mode="after")
    def validate_update(self):
        if not self.username and not self.email and not self.password:
            raise ValueError("data was not provided.")

        if self.email and not self.password:
            raise ValueError("when changing email, password must be provided.")
        
        return self

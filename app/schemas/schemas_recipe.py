from pydantic import EmailStr, BaseModel, field_validator
from uuid import UUID

class CreateUser(BaseModel):
    username: str
    email: EmailStr
    password: str

    @field_validator("username")
    def capitalize(cls, value):
        return value.title()

class User(CreateUser):
    id: UUID

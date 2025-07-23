import crud.crud as crud_operations
from fastapi import Depends, APIRouter
from schemas.schemas_recipe import CreateUser, User
from sqlmodel import Session
from db.db import get_session
from uuid import UUID

user_router = APIRouter(prefix="/users")


@user_router.post("/create_user")
def create_user(user: CreateUser, session: Session = Depends(get_session)) -> User:
    return crud_operations.create_new_user(user, session)

@user_router.delete("/delete_user/{user_id}")
def delete_user(user_id: UUID, session: Session = Depends(get_session)) -> str:
    return crud_operations.delete_user(user_id, session)

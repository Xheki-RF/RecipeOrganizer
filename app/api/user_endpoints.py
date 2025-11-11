import app.crud.crud as crud_operations
from fastapi import Depends, APIRouter
from app.schemas.schemas_recipe import CreateUser, User, UpdateUser
from sqlmodel import Session
from app.db.db import get_session
from uuid import UUID

user_router = APIRouter(prefix="/users")


@user_router.post("/create_user")
def create_user(user: CreateUser, session: Session = Depends(get_session)) -> User:
    return crud_operations.create_new_user(user, session)

@user_router.delete("/delete_user/{user_id}")
def delete_user(user_id: UUID, session: Session = Depends(get_session)) -> str:
    return crud_operations.delete_user(user_id, session)

@user_router.get("/get_users")
def get_users(session: Session = Depends(get_session)) -> list[User]:
    return crud_operations.get_users(session)

@user_router.patch("/update_user_data/{user_id}")
def update_user(user_id: UUID, data: UpdateUser, session: Session = Depends(get_session)) -> User:
    return crud_operations.update_user_data(user_id, data, session)

@user_router.get("/get_user/{user_id}")
def get_user(user_id: UUID, session: Session = Depends(get_session)) -> User:
    return crud_operations.get_user(user_id, session)
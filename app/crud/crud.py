from sqlmodel import Session, select
from schemas.schemas_recipe import *
from uuid import UUID
from db.db import get_session
from fastapi import HTTPException, status
from models.models_recipe import User


def create_new_user(user: CreateUser, session: Session) -> User:
    existing_user = session.exec(select(User).where(User.email == user.email)).first()

    if existing_user:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "The user with this email already exists.")
    
    new_user = User(**user.model_dump())

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user


def delete_user(user_id: UUID, session: Session) -> str:
    user_to_delete = session.exec(select(User).where(User.id == user_id)).first()

    session.delete(user_to_delete)
    session.commit()

    return f"User {user_to_delete.username} with ID {user_to_delete.id} has been deleted"

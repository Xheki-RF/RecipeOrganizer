from sqlmodel import Session, select
import schemas.schemas_recipe as schemas
from uuid import UUID
from fastapi import HTTPException, status
from models.models_recipe import User
import bcrypt


def create_new_user(user: schemas.CreateUser, session: Session) -> schemas.User:
    existing_user = session.exec(select(User).where(User.email == user.email)).first()

    if existing_user:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "The user with this email already exists.")

    new_user = User(**user.model_dump())
    new_user.password = bcrypt.hashpw(new_user.password, bcrypt.gensalt(12))

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user


def delete_user(user_id: UUID, session: Session) -> str:
    user_to_delete = session.exec(select(User).where(User.id == user_id)).first()

    session.delete(user_to_delete)
    session.commit()

    return f"User {user_to_delete.username} with ID {user_to_delete.id} has been deleted"


def get_users(session: Session) -> list[schemas.User]:
    all_users = session.exec(select(User)).all()

    return all_users


def update_user_data(user_id: UUID, data: schemas.UpdateUser, session: Session) -> schemas.User:
    user_to_update = session.exec(select(User).where(User.id == user_id)).first()

    if not user_to_update:
        raise ValueError("User not found.")

    if data.username:
        user_to_update.username = data.username

    if data.email:
        user_to_update.email = data.email

    if data.password:
        user_to_update.password = data.password

    session.add(user_to_update)
    session.commit()
    session.refresh(user_to_update)

    return user_to_update


def get_user(user_id: UUID, session: Session) -> schemas.User:
    user_to_get = session.exec(select(User).where(User.id == user_id)).first()

    return user_to_get

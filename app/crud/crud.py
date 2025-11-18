from sqlmodel import Session, select
import app.schemas.schemas_recipe as schemas
from uuid import UUID
from fastapi import HTTPException, status
from app.models.models_recipe import User, Recipe
import bcrypt


def create_new_user(user: schemas.CreateUser, session: Session) -> schemas.User:
    existing_user = session.exec(select(User).where(User.email == user.email)).first()

    if existing_user:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "The user with this email already exists.")

    new_user = User(**user.model_dump())
    new_user.password = bcrypt.hashpw(new_user.password.encode("utf-8"), bcrypt.gensalt(12))

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
        user_to_update.password = bcrypt.hashpw(data.password.encode("utf-8"), bcrypt.gensalt(12))

    session.add(user_to_update)
    session.commit()
    session.refresh(user_to_update)

    return user_to_update


def get_user(user_id: UUID, session: Session) -> schemas.User:
    user_to_get = session.exec(select(User).where(User.id == user_id)).first()

    return user_to_get


def add_recipe(recipe_data: schemas.CreateRecipe, session: Session) -> schemas.Recipe:
    new_recipe = Recipe(**recipe_data.model_dump())

    session.add(new_recipe)
    session.commit()
    session.refresh(new_recipe)

    return new_recipe


def delete_recipe(recipe_id: UUID, session: Session) -> str:
    recipe_to_delete = session.exec(select(Recipe).where(Recipe.id == recipe_id)).first()

    session.delete(recipe_to_delete)
    session.commit()

    return f"Recipe {recipe_to_delete.title} with ID {recipe_to_delete.id} has been deleted"


def get_user_recipes(user_id: UUID, session: Session) -> list[Recipe]:
    user_recipes = session.exec(select(Recipe).where(Recipe.user_id == user_id)).all()

    return user_recipes


def update_user_recipe(user_id: UUID, recipe_data: schemas.UpdateRecipe, session: Session) -> schemas.Recipe:
    recipe_to_update = session.exec(select(Recipe).where((Recipe.user_id == user_id) & (Recipe.id == recipe_data.id))).first()

    if recipe_data.title:
        recipe_to_update.title = recipe_data.title

    if recipe_data.description:
        recipe_to_update.description = recipe_data.description

    if recipe_data.category_id:
        recipe_to_update.category_id = recipe_data.category_id

    session.add(recipe_to_update)
    session.commit()
    session.refresh(recipe_to_update)

    return recipe_to_update

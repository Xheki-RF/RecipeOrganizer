import app.crud.crud as crud
from fastapi import Depends, APIRouter
from app.schemas.schemas_recipe import CreateRecipe, Recipe, UpdateRecipe
from sqlmodel import Session
from app.db.db import get_session
from uuid import UUID


recipe_router = APIRouter(prefix="/recipe")


@recipe_router.post("/add_recipe")
def add_recipe(recipe: CreateRecipe, session: Session = Depends(get_session)) -> Recipe:
    return crud.add_recipe(recipe, session)


@recipe_router.delete("/delete_recipe/{recipe_id}")
def delete_recipe(recipe_id: UUID, session: Session = Depends(get_session)) -> str:
    return crud.delete_recipe(recipe_id, session)


@recipe_router.get("/get_user_recipes/{user_id}")
def get_user_recipes(user_id: UUID, session: Session = Depends(get_session)) -> list[Recipe]:
    return crud.get_user_recipes(user_id, session)


@recipe_router.patch("/update_user_recipe/{recipe_id}")
def update_user_recipe(recipe_id: UUID, recipe_data: UpdateRecipe, session: Session = Depends(get_session)) -> Recipe:
    return crud.update_user_recipe(recipe_id, recipe_data, session)


@recipe_router.get("/get_user_recipe/{recipe_id}")
def get_user_recipe(recipe_id: UUID, session: Session = Depends(get_session)):
    return crud.get_user_recipe(recipe_id, session)
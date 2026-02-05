from datetime import datetime, timezone
import uuid
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from uuid import UUID
from enum import Enum
import sqlalchemy as sa
from sqlalchemy.orm import backref


def get_local_time():
    return datetime.now()


class User(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    username: str
    email: str
    password: str

    date_created: datetime = Field(default_factory=get_local_time)
    last_updated: datetime = Field(sa_column=sa.Column(
        sa.DateTime, 
        default=get_local_time, 
        onupdate=get_local_time
        )
    )

    recipes: list["Recipe"] = Relationship(back_populates="user", cascade_delete=True)


class CategoryEnum(str, Enum):
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    SUPPER = "supper"
    DESSERT = "dessert"
    SNACK = "snack"


class Category(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    name: CategoryEnum = Field(index=True, unique=True)

    recipes: list["Recipe"] = Relationship(back_populates="category")


class Recipe(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str
    description: str

    user_id: UUID = Field(foreign_key="user.id", )
    category_id: UUID = Field(foreign_key="category.id")

    date_added: datetime = Field(default_factory=get_local_time)
    last_updated: datetime = Field(
        sa_column=sa.Column(
            sa.DateTime,
            default=get_local_time,
            onupdate=get_local_time
        )
    )

    user: Optional[User] = Relationship(back_populates="recipes")
    category: Optional[Category] = Relationship(back_populates="recipes")
    ingredients: list["Ingredient"] = Relationship(back_populates="recipe")


class Ingredient(SQLModel, table=True):
    id: Optional[UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str
    amount: str
    recipe_id: UUID = Field(foreign_key="recipe.id")

    recipe: Optional[Recipe] = Relationship(back_populates="ingredients")

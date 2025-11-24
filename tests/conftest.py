import pytest
from fastapi.testclient import TestClient
from app.main import app
from sqlmodel import SQLModel, Session, create_engine
from app.db.db import get_session
from sqlalchemy.pool import StaticPool
from app.models.models_recipe import User, Ingredient, Category, Recipe
import app.db.db as db_module


# Use a temporary in-memory database for tests
TEST_DATABASE_URL = "sqlite:///:memory:"
ram_engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)
db_module.engine = ram_engine


# Override FastAPI's dependency
def override_get_session():
    with Session(ram_engine) as session:
        yield session


app.dependency_overrides[get_session] = override_get_session

@pytest.fixture(scope="function", autouse=True)
def setup_database():
    SQLModel.metadata.create_all(ram_engine)
    yield
    SQLModel.metadata.drop_all(ram_engine)


@pytest.fixture(scope="function")
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="function")
def create_users():
    def _create_user(single=True):
        if single:
            users_data = {
                "username": "Jane Doe",
                "email": "zenlesszone@gmail.com",
                "password": "furrylover",
            }

        else:
            users_data = [
                {
                    "username": "Jane Doe",
                    "email": "zenlesszone@gmail.com",
                    "password": "furrylover",
                },
                {
                    "username": "Avian Birb",
                    "email": "birb69@gmail.com",
                    "password": "avianlover",
                },
            ]

        return users_data

    return _create_user


@pytest.fixture(scope="function")
def add_recipe():
    def _add_recipe(single=True):
        if single:
            recipes_data = {
                "title": "Bread",
                "description": "Allows you to make a fluffy bread",
                "category_id": "c0a03644-b2c7-4c71-bb31-fa4358c36f45",
            }
        else:
            recipes_data = [
                {
                    "title": "Bread",
                    "description": "Allows you to make a fluffy bread",
                    "category_id": "c0a03644-b2c7-4c71-bb31-fa4358c36f45",
                },
                {
                    "title": "Chocolate",
                    "description": "Allows you to make a milk chocolate",
                    "category_id": "1dd2c417-45c6-4875-a8ff-d5c1621c5804",
                },
            ]

        return recipes_data

    return _add_recipe

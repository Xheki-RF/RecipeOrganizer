import pytest
from fastapi.testclient import TestClient
from main import app
from sqlmodel import SQLModel, Session, create_engine, select
from app.db.db import get_session
from sqlalchemy.pool import StaticPool
from app.models.models_recipe import User, Ingredient, Category, Recipe
import app.db.db as db_module
from app.db.db import get_session
from app.models.models_recipe import Category, CategoryEnum


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

    with Session(ram_engine) as session:
        for c in CategoryEnum:
            session.add(Category(name=c))
            
        session.commit()

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
def get_category_id():
    def _get_category_id(category_name):
        session: Session = next(get_session())
        
        category_id = session.exec(select(Category).where(Category.name == category_name)).first()

        return str(category_id.id)
    
    return _get_category_id


@pytest.fixture(scope="function")
def add_recipe(get_category_id):
    def _add_recipe(single=True):
        if single:
            recipes_data = {
                "title": "Bread",
                "description": "Allows you to make a fluffy bread",
                "category_id": get_category_id("breakfast"),
            }
        else:
            recipes_data = [
                {
                    "title": "Bread",
                    "description": "Allows you to make a fluffy bread",
                    "category_id": get_category_id("breakfast"),
                },
                {
                    "title": "Chocolate",
                    "description": "Allows you to make a milk chocolate",
                    "category_id": get_category_id("lunch"),
                },
            ]

        return recipes_data

    return _add_recipe

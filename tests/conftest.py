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


@pytest.fixture()
def client():
    with TestClient(app) as c:
        yield c

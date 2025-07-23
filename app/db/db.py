from sqlmodel import create_engine, SQLModel, Session
import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DB_URL")

if DB_URL is None:
    raise ValueError("DB_URL environment variable not set!")

engine = create_engine(DB_URL, echo=False)

def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

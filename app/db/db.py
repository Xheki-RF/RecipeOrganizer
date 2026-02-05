from sqlmodel import create_engine, SQLModel, Session
import os
from dotenv import load_dotenv

load_dotenv()

DB_URL = os.getenv("DB_URL")

if DB_URL is None:
    try:
        # For pytest
        DB_URL = f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}@localhost/{os.environ['POSTGRES_DB']}"
    except:
        raise ValueError("DB_URL environment variable is not set!")

engine = create_engine(DB_URL, echo=False)

def init_db():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

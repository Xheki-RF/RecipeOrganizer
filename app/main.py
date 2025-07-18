from fastapi import FastAPI
import uvicorn
from db.db import init_db
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)

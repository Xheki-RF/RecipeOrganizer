from fastapi import FastAPI
import uvicorn
from app.db.db import init_db
from contextlib import asynccontextmanager
from app.api.user_endpoints import *


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)

app.include_router(user_router)

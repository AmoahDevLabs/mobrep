from contextlib import asynccontextmanager
from fastapi import FastAPI

from .database import init_db
from .views import users, tellers, transactions


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(
    title="MOBREP – Mobile Banking Records",
    version="1.0.0",
    lifespan=lifespan,
)


# Register routers
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(tellers.router, prefix="/tellers", tags=["Tellers"])
app.include_router(
    transactions.router,
    prefix="/transactions",
    tags=["Transactions"],
)

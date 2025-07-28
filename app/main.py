from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI

from api.aggregates import router as aggregates_router
from api.patterns import router as patterns_router


async def startup():
    print("starting up")


async def shutdown():
    print("shutting down")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await startup()
    yield
    await shutdown()


app = FastAPI(lifespan=lifespan)


api_router = APIRouter(prefix="/api")

api_router.include_router(aggregates_router, prefix="/aggregates")
api_router.include_router(patterns_router, prefix="/patterns")

app.include_router(api_router)

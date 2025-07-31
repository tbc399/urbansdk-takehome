from fastapi import APIRouter, FastAPI

from app.api.aggregates import router as aggregates_router
from app.api.patterns import router as patterns_router

app = FastAPI()


api_router = APIRouter(prefix="/api")

api_router.include_router(aggregates_router, prefix="/aggregates")
api_router.include_router(patterns_router, prefix="/patterns")

app.include_router(api_router)

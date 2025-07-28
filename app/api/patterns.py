from fastapi import APIRouter

router = APIRouter()


@router.get("/slow_links")
async def get():
    return "Slow Links"

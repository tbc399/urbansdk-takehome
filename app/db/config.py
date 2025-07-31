from functools import cache
from typing import Annotated

from fastapi import Depends
from sqlalchemy import URL, Engine, create_engine
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine

from app.config import settings


@cache
def get_engine() -> AsyncEngine:
    url = URL.create(
        "postgresql+asyncpg",
        username=settings().db_username,
        password=settings().db_pass,
        host=settings().db_host,
        database=settings().db_name,
    )
    return create_async_engine(url)


async def _get_session():
    async with AsyncSession(get_engine()) as session:
        yield session


DbSession = Annotated[AsyncSession, Depends(_get_session)]

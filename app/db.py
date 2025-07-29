from sqlalchemy import create_engine, URL, Engine
from functools import cache
from settings import get_settings


@cache
def engine() -> Engine:
    settings = get_settings()
    url = URL.create(
        "postgresql",
        username=settings.db_username,
        password=settings.db_pass,
        host=settings.db_host,
        database=settings.db_name,
    )
    return create_engine(url)

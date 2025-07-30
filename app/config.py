from functools import cache
from typing import Annotated

from fastapi import Depends
from pydantic_settings import BaseSettings
from sqlalchemy import URL, Engine, create_engine
from sqlalchemy.orm import Session


class Settings(BaseSettings):
    db_username: str
    db_pass: str
    db_host: str
    db_name: str


@cache
def settings() -> Settings:
    return Settings()


@cache
def get_engine() -> Engine:
    url = URL.create(
        "postgresql+psycopg",
        username=settings().db_username,
        password=settings().db_pass,
        host=settings().db_host,
        database=settings().db_name,
    )
    return create_engine(url)


def _get_session():
    with Session(get_engine()) as session:
        yield session


DbSession = Annotated[Session, Depends(_get_session)]

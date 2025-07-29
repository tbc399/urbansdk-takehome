from functools import cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_username: str
    db_pass: str
    db_host: str
    db_name: str


@cache
def settings() -> Settings:
    return Settings()

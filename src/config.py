from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    api_str: str = "/api"
    database_url: str = "sqlite:///./storage.db"
    access_token_expire_minutes: int = 60 * 8
    secret_key: str = "648e21294aca7ec16b7eeecda82e070782fc0059cb7bd4ae02c7de1a7e1e3737"
    jwt_algorithm: str = "HS256"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()

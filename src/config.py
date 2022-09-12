from functools import lru_cache

from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    api_str: str = "/api"
    access_token_expire_minutes: int = 60 * 8
    secret_key: str = "648e21294aca7ec16b7eeecda82e070782fc0059cb7bd4ae02c7de1a7e1e3737"
    jwt_algorithm: str = "HS256"
    rds_hostname: str = None
    rds_user: str = None
    rds_port: str = None
    rds_db: str = None
    rds_password: str = None

    @property
    def database_url(self) -> str:
        if all([self.rds_hostname, self.rds_user, self.rds_port, self.rds_db]):
            return f"postgresql://{self.rds_user}:{self.rds_password}@{self.rds_hostname}:{self.rds_port}/{self.rds_db}"
        return "sqlite:///./storage.db"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()

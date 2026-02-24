from pydantic_settings import BaseSettings
from functools import lru_cache 

class Settings(BaseSettings):

    app_name: str = "Task Manger API"
    app_version: str = "0.1.0"
    debug: bool = False

    database_url: str = "sqlite:///./task_manager.db"

    secret_key: str = "notforpublicsecretkey"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    cors_origins: list[str] = [
        "http://localhost:3000"
    ]

    class Config:        
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

@lru_cache
def get_settings() -> Settings:
    return settings
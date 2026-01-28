from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    ENVIRONMENT: str = "development"
    DATABASE_URL: Optional[str] = None
    LARAVEL_GATEWAY_URL: str = "http://localhost:8000"
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "ContentIQ"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    
    # Database
    MONGODB_URL: str = "mongodb://127.0.0.1:27017"
    DATABASE_NAME: str = "contentiq"
    
    # Redis
    REDIS_URL: str = "redis://127.0.0.1:6379/0"
    
    # Security
    SECRET_KEY: str = "contentiq-super-secret-jwt-token-key-mca-final-year-2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 1 day

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()

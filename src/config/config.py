from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, validator
from typing import List, Optional, Union
import os

class Settings(BaseSettings):
    PROJECT_NAME: str = "nutrivue"
    PROJECT_DESCRIPTION: str = "Industry-grade Calorie Monitor"
    VERSION: str = "1.0.0"
    
    API_V1_STR: str = "/api/v1"
    ENV:str # or maybe Optional[str]
    # Server configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = os.getenv("ENV", "dev") == "dev"
    WORKERS: int = 1 if RELOAD else 4
    
    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:5173",  # Default frontend URL
    ]
    
    # Firebase
    FIREBASE_CREDENTIALS_PATH: str = "./serviceAccountKey.json"
    DATABASE_URL_SYNC:str
    DATABASE_URL_ASYNC:str
    DB_USER:str
    DB_PASSWORD:str
    DB_HOST:str
    DB_PORT:str
    DB_NAME:str
    GOOGLE_API_KEY: str
    REDIS_URL: str
    CACHE_EXPIRE_HOURS: int
    class Config:
        case_sensitive = True
        env_file = ".env"

def get_settings():
    return Settings()
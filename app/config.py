from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # App Settings
    APP_NAME: str = "Expense Tracker API"
    API_V1_STR: str = "/api/v1"
    
    # Security Settings
    SECRET_KEY: str = "YOUR_SECRET_KEY_HERE"  # Change in production!
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Database Settings
    DATABASE_URL: str = "sqlite:///./expense_tracker.db"
    
    class Config:
        env_file = ".env"


settings = Settings()
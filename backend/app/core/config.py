from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    APP_NAME: str = "Tax Filing Automation System"
    DEBUG: bool = True
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    GROQ_API_KEY: Optional[str] = None
    GROQ_MODEL: str = "llama-3.3-70b-versatile"
    UPLOAD_DIR: str = "./uploads"
    MAX_FILE_SIZE: int = 10485760
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"

settings = Settings()

TAX_SLABS = {
    "slabs": [
        {"min": 0, "max": 600000, "rate": 0, "fixed": 0},
        {"min": 600001, "max": 1200000, "rate": 0.025, "fixed": 0},
        {"min": 1200001, "max": 2400000, "rate": 0.125, "fixed": 15000},
        {"min": 2400001, "max": 3600000, "rate": 0.20, "fixed": 165000},
        {"min": 3600001, "max": 6000000, "rate": 0.25, "fixed": 405000},
        {"min": 6000001, "max": 12000000, "rate": 0.325, "fixed": 1005000},
        {"min": 12000001, "max": 999999999, "rate": 0.35, "fixed": 2955000}
    ]
}

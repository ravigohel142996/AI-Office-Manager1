"""Configuration settings for the AI Office Manager"""
import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """Application settings"""
    
    # API Configuration
    API_TITLE = "AI Office Manager API"
    API_VERSION = "1.0.0"
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", "8000"))
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ai_office_manager.db")
    
    # Security
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    
    # OpenAI
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    USE_MOCK_AI = os.getenv("USE_MOCK_AI", "true").lower() == "true"
    
    # App Settings
    DEBUG = os.getenv("DEBUG", "true").lower() == "true"

settings = Settings()

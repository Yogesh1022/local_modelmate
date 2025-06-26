# backend/config.py

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()  # Load .env file before reading settings

class Settings(BaseSettings):
    # MongoDB connection
    MONGO_URI: str = "mongodb://localhost:27017"
    MONGO_DB_NAME: str = "modelmate"  # ✅ Default fallback

    # JWT secret and expiry
    JWT_SECRET: str = "supersecretkey"
    JWT_EXPIRY: int = 3600  # seconds

    # Together.AI
    TOGETHER_API_KEY: str = ""

    # PlantUML JAR path
    PLANTUML_JAR_PATH: str = "backend/utils/plantuml.jar"

    class Config:
        env_file = ".env"

# ✅ Create global settings object
settings = Settings()

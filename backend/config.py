# backend/config.py
import os
import logging
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, AnyUrl, validator
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("modelmate_config.log")
    ]
)
logger = logging.getLogger(__name__)

# Load environment variables
try:
    load_dotenv(override=True)
    logger.info("Environment variables loaded successfully")
except Exception as e:
    logger.error(f"Failed to load .env file: {str(e)}")
    raise

class Settings(BaseSettings):
    # MongoDB connection
    MONGO_URI: str = Field(
        default="mongodb://localhost:27017",
        description="MongoDB connection URI"
    )
    MONGO_DB_NAME: str = Field(
        default="modelmate",
        description="MongoDB database name"
    )
    USERS_COLLECTION: str = Field(
        default="users",
        description="MongoDB collection name for users"
    )

    # JWT settings
    JWT_SECRET: str = Field(
        default="supersecretkey",
        min_length=32,
        description="JWT secret key for token signing"
    )
    JWT_EXPIRY: int = Field(
        default=3600,
        ge=60,
        description="JWT token expiry time in seconds"
    )

    # Together.AI
    TOGETHER_API_KEY: str = Field(
        default="",
        description="Together.AI API key"
    )

    # PlantUML JAR path
    PLANTUML_JAR_PATH: str = Field(
        default="backend/utils/plantuml.jar",
        description="Path to PlantUML JAR file"
    )

    # Dataset path for research
    DATASET_PATH: str = Field(
        default=str(Path(__file__).resolve().parent.parent / "data" / "project_dataset" / "academic_projects.json"),
        description="Path to dataset file for research"
    )

    # Research settings
    RESEARCH_MAX_RESULTS: int = Field(
        default=10,
        ge=1,
        le=20,
        description="Maximum number of research results to return"
    )

    # Validate MongoDB URI format
    @validator("MONGO_URI")
    def validate_mongo_uri(cls, value: str) -> str:
        if not value.startswith("mongodb://") and not value.startswith("mongodb+srv://"):
            logger.error("Invalid MongoDB URI format")
            raise ValueError("MONGO_URI must start with 'mongodb://' or 'mongodb+srv://'")
        return value

    # Validate PlantUML JAR path
    @validator("PLANTUML_JAR_PATH")
    def validate_plantuml_path(cls, value: str) -> str:
        if not os.path.isfile(value):
            logger.warning(f"PlantUML JAR file not found at: {value}")
        return value

    # Validate JWT secret strength
    @validator("JWT_SECRET")
    def validate_jwt_secret(cls, value: str) -> str:
        if value == "supersecretkey" and os.getenv("ENV") != "development":
            logger.warning("Using default JWT_SECRET in non-development environment")
        return value

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

try:
    settings = Settings()
    logger.info("Settings initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize settings: {str(e)}")
    raise
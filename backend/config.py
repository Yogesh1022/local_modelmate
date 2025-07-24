# import logging
# import os
# from typing import Optional
# from pydantic_settings import BaseSettings, SettingsConfigDict
# from pydantic import Field, AnyUrl, validator
# from dotenv import load_dotenv

# # Configure logging
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
#     handlers=[
#         logging.StreamHandler(),
#         logging.FileHandler("modelmate_config.log")
#     ]
# )
# logger = logging.getLogger(__name__)

# # Load environment variables
# try:
#     load_dotenv(override=True)  # Load .env file with override for precedence
#     logger.info("Environment variables loaded successfully")
# except Exception as e:
#     logger.error(f"Failed to load .env file: {str(e)}")
#     raise

# class Settings(BaseSettings):
#     # MongoDB connection
#     MONGO_URI: str = Field(
#         default="mongodb://localhost:27017",
#         description="MongoDB connection URI"
#     )
#     MONGO_DB_NAME: str = Field(
#         default="modelmate",
#         description="MongoDB database name"
#     )
#     USERS_COLLECTION: str = Field(  # New field
#         default="users",
#         description="MongoDB collection name for users"
#     )

#     # JWT settings
#     JWT_SECRET: str = Field(
#         default="supersecretkey",
#         min_length=32,  # Enforce minimum length for security
#         description="JWT secret key for token signing"
#     )
#     JWT_EXPIRY: int = Field(
#         default=3600,  # 1 hour
#         ge=60,  # Minimum 60 seconds
#         description="JWT token expiry time in seconds"
#     )

#     # OTP settings
#     OTP_ISSUER: str = Field(
#         default="ModelMate",
#         description="OTP issuer name"
#     )
#     OTP_LENGTH: int = Field(
#         default=6,
#         ge=4,
#         le=8,
#         description="Length of OTP"
#     )
#     OTP_TTL: int = Field(
#         default=300,
#         ge=60,
#         description="OTP time to live in seconds"
#     )

#     # Together.AI
#     TOGETHER_API_KEY: Optional[str] = Field(
#         default="",
#         description="Together.AI API key"
#     )

#     # PlantUML JAR path
#     PLANTUML_JAR_PATH: str = Field(
#         default="backend/utils/plantuml.jar",
#         description="Path to PlantUML JAR file"
#     )

#     # Validate MongoDB URI format
#     @validator("MONGO_URI")
#     def validate_mongo_uri(cls, value: str) -> str:
#         if not value.startswith("mongodb://") and not value.startswith("mongodb+srv://"):
#             logger.error("Invalid MongoDB URI format")
#             raise ValueError("MONGO_URI must start with 'mongodb://' or 'mongodb+srv://'")
#         return value

#     # Validate PlantUML JAR path
#     @validator("PLANTUML_JAR_PATH")
#     def validate_plantuml_path(cls, value: str) -> str:
#         if not os.path.isfile(value):
#             logger.warning(f"PlantUML JAR file not found at: {value}")
#         return value
    
#     # Validate dataset path
#     @validator("DATASET_PATH")
#     def validate_dataset_path(cls, value: str) -> str:
#         dataset_dir = Path(value).parent
#         if not dataset_dir.exists():
#             logger.warning(f"Dataset directory not found at: {dataset_dir}")
#             dataset_dir.mkdir(parents=True, exist_ok=True)
#         return value

#     # Validate JWT secret strength
#     @validator("JWT_SECRET")
#     def validate_jwt_secret(cls, value: str) -> str:
#         if value == "supersecretkey" and os.getenv("ENV") != "development":
#             logger.warning("Using default JWT_SECRET in non-development environment")
#         return value

#     model_config = SettingsConfigDict(
#         env_file=".env",
#         env_file_encoding="utf-8",
#         case_sensitive=False,  # Allow case-insensitive env variables
#         extra="ignore"  # Ignore unknown env variables
#     )

# # Create global settings object
# try:
#     settings = Settings()
#     logger.info("Settings initialized successfully")
# except Exception as e:
#     logger.error(f"Failed to initialize settings: {str(e)}")
#     raise


# # added otp issuer to settings and otp lenggth olsp ttl and enhance daset path



# import logging
# import os
# from typing import Optional
# from pydantic_settings import BaseSettings, SettingsConfigDict
# from pydantic import Field, validator
# from dotenv import load_dotenv
# from pathlib import Path

# # Configure logging
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
#     handlers=[
#         logging.StreamHandler(),
#         logging.FileHandler("modelmate_config.log")
#     ]
# )
# logger = logging.getLogger(__name__)

# # Load environment variables
# try:
#     load_dotenv(override=True)
#     logger.info("Environment variables loaded successfully")
# except Exception as e:
#     logger.error(f"Failed to load .env file: {str(e)}")
#     raise

# class Settings(BaseSettings):
#     # MongoDB connection
#     MONGO_URI: str = Field(
#         default="mongodb://localhost:27017",
#         description="MongoDB connection URI"
#     )
#     MONGO_DB_NAME: str = Field(
#         default="modelmate",
#         description="MongoDB database name"
#     )
#     USERS_COLLECTION: str = Field(
#         default="users",
#         description="MongoDB collection name for users"
#     )
    
#     # NEW: MongoDB collection for storing prompt results
#     PROMPT_RESULTS_COLLECTION: str = Field(
#         default="prompt_results",
#         description="MongoDB collection name for storing LLM prompt results"
#     )

#     # JWT settings
#     JWT_SECRET: str = Field(
#         default="supersecretkey",
#         min_length=32,
#         description="JWT secret key for token signing"
#     )
#     JWT_EXPIRY: int = Field(
#         default=3600,
#         ge=60,
#         description="JWT token expiry time in seconds"
#     )

#     # OTP settings
#     OTP_ISSUER: str = Field(
#         default="ModelMate",
#         description="OTP issuer name"
#     )
#     OTP_LENGTH: int = Field(
#         default=6,
#         ge=4,
#         le=8,
#         description="Length of OTP"
#     )
#     OTP_TTL: int = Field(
#         default=300,
#         ge=60,
#         description="OTP time to live in seconds"
#     )
#     OTP_COLLECTION: str = Field(
#         default="otp_records",
#         description="MongoDB collection name for OTP records"
#     )

#     # Together.AI settings
#     TOGETHER_API_KEY: Optional[str] = Field(
#         default="",
#         description="Together.AI API key"
#     )
    
#     # NEW: Default LLM model and parameters
#     LLM_DEFAULT_MODEL: str = Field(
#         default="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
#         description="Default LLM model for prompt processing"
#     )
#     LLM_DEFAULT_TEMPERATURE: float = Field(
#         default=0.7,
#         ge=0.0,
#         le=1.0,
#         description="Default temperature for LLM generation"
#     )
#     LLM_DEFAULT_MAX_TOKENS: int = Field(
#         default=1024,
#         ge=1,
#         description="Default max tokens for LLM response"
#     )

#     # PlantUML JAR path
#     PLANTUML_JAR_PATH: str = Field(
#         default="backend/utils/plantuml.jar",
#         description="Path to PlantUML JAR file"
#     )

#     # Dataset path
#     DATASET_PATH: str = Field(
#         default="data/academic_projects.json",
#         description="Path to the dataset file"
#     )

#     # SMTP Email settings
#     SMTP_SERVER: Optional[str] = Field(
#         default=None,
#         description="SMTP server address"
#     )
#     SMTP_PORT: Optional[int] = Field(
#         default=587,
#         description="SMTP server port"
#     )
#     SMTP_SENDER_EMAIL: Optional[str] = Field(
#         default=None,
#         description="Sender email address for SMTP"
#     )
#     SMTP_SENDER_PASSWORD: Optional[str] = Field(
#         default=None,
#         description="Password for sender email"
#     )

#     # Validate MongoDB URI format
#     @validator("MONGO_URI")
#     def validate_mongo_uri(cls, value: str) -> str:
#         if not value.startswith("mongodb://") and not value.startswith("mongodb+srv://"):
#             logger.error("Invalid MongoDB URI format")
#             raise ValueError("MONGO_URI must start with 'mongodb://' or 'mongodb+srv://'")
#         return value

#     # Validate PlantUML JAR path
#     @validator("PLANTUML_JAR_PATH")
#     def validate_plantuml_path(cls, value: str) -> str:
#         if not os.path.isfile(value):
#             logger.warning(f"PlantUML JAR file not found at: {value}")
#         return value
    
#     # Validate dataset path
#     @validator("DATASET_PATH")
#     def validate_dataset_path(cls, value: str) -> str:
#         dataset_dir = Path(value).parent
#         if not dataset_dir.exists():
#             logger.warning(f"Dataset directory not found at: {dataset_dir}")
#             dataset_dir.mkdir(parents=True, exist_ok=True)
#         return value

#     # Validate JWT secret strength
#     @validator("JWT_SECRET")
#     def validate_jwt_secret(cls, value: str) -> str:
#         if value == "supersecretkey" and os.getenv("ENV") != "development":
#             logger.warning("Using default JWT_SECRET in non-development environment")
#         return value

#     model_config = SettingsConfigDict(
#         env_file=".env",
#         env_file_encoding="utf-8",
#         case_sensitive=False,
#         extra="ignore"
#     )

# # Create global settings object
# try:
#     settings = Settings()
#     logger.info("Settings initialized successfully")
# except Exception as e:
#     logger.error(f"Failed to initialize settings: {str(e)}")
#     raise

import logging
import os
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, validator
from dotenv import load_dotenv
from pathlib import Path

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

# ✅ FIX: Explicitly define the path to the .env file in the parent directory
# This makes sure the app can find your credentials regardless of where you run it
env_path = Path('.') / '.env'


# Load environment variables
try:
    load_dotenv(dotenv_path=env_path, override=True)
    logger.info("Environment variables loaded successfully")
except Exception as e:
    logger.error(f"Failed to load .env file: {str(e)}")
    raise

class Settings(BaseSettings):
    # MongoDB connection
    MONGO_URI: str = Field(..., description="MongoDB connection URI")
    MONGO_DB_NAME: str = Field(..., description="MongoDB database name")
    USERS_COLLECTION: str = Field("users", description="MongoDB collection name for users")
    PROMPT_RESULTS_COLLECTION: str = Field("prompt_results", description="MongoDB collection name for storing LLM prompt results")

    # JWT settings
    JWT_SECRET: str = Field(..., min_length=32, description="JWT secret key for token signing")
    JWT_EXPIRY: int = Field(3600, ge=60, description="JWT token expiry time in seconds")

    # OTP settings
    OTP_ISSUER: str = Field("ModelMate", description="OTP issuer name")
    OTP_LENGTH: int = Field(6, ge=4, le=8, description="Length of OTP")
    OTP_TTL: int = Field(300, ge=60, description="OTP time to live in seconds")
    OTP_COLLECTION: str = Field("otp_records", description="MongoDB collection name for OTP records")

    # Together.AI settings
    TOGETHER_API_KEY: Optional[str] = Field(None, description="Together.AI API key")
    
    # Default LLM model and parameters
    LLM_DEFAULT_MODEL: str = Field("meta-llama/Llama-3.3-70B-Instruct-Turbo-Free", description="Default LLM model for prompt processing")
    LLM_DEFAULT_TEMPERATURE: float = Field(0.7, ge=0.0, le=1.0, description="Default temperature for LLM generation")
    LLM_DEFAULT_MAX_TOKENS: int = Field(1024, ge=1, description="Default max tokens for LLM response")

    # PlantUML JAR path
    PLANTUML_JAR_PATH: str = Field("backend/utils/plantuml.jar", description="Path to PlantUML JAR file")

    # Dataset path
    DATASET_PATH: str = Field("data/academic_projects.json", description="Path to the dataset file")

    # SMTP Email settings
    SMTP_SERVER: Optional[str] = Field(None, description="SMTP server address")
    SMTP_PORT: Optional[int] = Field(587, description="SMTP server port")
    SMTP_SENDER_EMAIL: Optional[str] = Field(None, alias="EMAIL_USER", description="Sender email address for SMTP")
    SMTP_SENDER_PASSWORD: Optional[str] = Field(None, alias="EMAIL_PASS", description="Password for sender email")

    # Validators
    @validator("MONGO_URI")
    def validate_mongo_uri(cls, value: str) -> str:
        if not value.startswith("mongodb://") and not value.startswith("mongodb+srv://"):
            logger.error("Invalid MongoDB URI format")
            raise ValueError("MONGO_URI must start with 'mongodb://' or 'mongodb+srv://'")
        return value

    @validator("PLANTUML_JAR_PATH")
    def validate_plantuml_path(cls, value: str) -> str:
        if not os.path.isfile(value):
            logger.warning(f"PlantUML JAR file not found at: {value}")
        return value
    
    @validator("DATASET_PATH")
    def validate_dataset_path(cls, value: str) -> str:
        dataset_dir = Path(value).parent
        if not dataset_dir.exists():
            logger.warning(f"Dataset directory not found at: {dataset_dir}")
            dataset_dir.mkdir(parents=True, exist_ok=True)
        return value

    @validator("JWT_SECRET")
    def validate_jwt_secret(cls, value: str) -> str:
        if value == "supersecretkey" and os.getenv("ENV") != "development":
            logger.warning("Using default JWT_SECRET in non-development environment")
        return value

    class Config:
        # ✅ FIX: Tell Pydantic exactly where to find the file
        env_file = env_path
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"
        populate_by_name = True


# Create global settings object
try:
    settings = Settings()
    logger.info("Settings initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize settings: {str(e)}")
    raise

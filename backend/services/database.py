# # backend/services/database.py
# from motor.motor_asyncio import AsyncIOMotorClient
# from backend.config import settings


# # ✅ Async MongoDB client using Motor with settings
# client = AsyncIOMotorClient(settings.MONGO_URI)
# db = client[settings.MONGO_DB_NAME]

# # Optional debug print
# print(f"✅ Connected to MongoDB: {db.name}")

# async def get_db():
#     """Yield the database instance for dependency injection."""
#     yield db

# async def get_collection(collection_name: str):
#     """Get a specific collection from the database."""
#     return db[collection_name]

from motor.motor_asyncio import AsyncIOMotorClient
from backend.config import settings
import logging

logger = logging.getLogger(__name__)

# Async MongoDB client using Motor with settings
client = AsyncIOMotorClient(settings.MONGO_URI)
db = client[settings.MONGO_DB_NAME]

# Optional debug print
print(f"✅ Connected to MongoDB: {db.name}")

async def get_db():
    """Yield the database instance for dependency injection."""
    return db

async def get_collection(collection_name: str):
    """Get a specific collection from the database."""
    return db[collection_name]

# NEW: Helper for prompt results collection
async def get_prompt_results_collection():
    """Get the prompt results collection."""
    return db[settings.PROMPT_RESULTS_COLLECTION]

# NEW: Helper for OTP collection
async def get_otp_collection():
    """Get the OTP collection."""
    return db[settings.OTP_COLLECTION]

# NEW: Initialize database indexes
async def initialize_database():
    """Initialize database collections and indexes."""
    try:
        # Create index for prompt results (user_id + prompt_hash)
        prompt_collection = await get_prompt_results_collection()
        await prompt_collection.create_index([("user_id", 1), ("prompt_hash", 1)], unique=True)
        
        # Create index for OTP collection (email + expiry)
        otp_collection = await get_otp_collection()
        await otp_collection.create_index([("email", 1)], unique=False)
        await otp_collection.create_index([("created_at", 1)], expireAfterSeconds=settings.OTP_TTL)
        
        logger.info("Database indexes created successfully")
    except Exception as e:
        logger.error(f"Error creating database indexes: {str(e)}")

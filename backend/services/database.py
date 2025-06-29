# backend/services/database.py
from motor.motor_asyncio import AsyncIOMotorClient
from backend.config import settings


# ✅ Async MongoDB client using Motor with settings
client = AsyncIOMotorClient(settings.MONGO_URI)
db = client[settings.MONGO_DB_NAME]

# Optional debug print
print(f"✅ Connected to MongoDB: {db.name}")

async def get_db():
    """Yield the database instance for dependency injection."""
    yield db

async def get_collection(collection_name: str):
    """Get a specific collection from the database."""
    return db[collection_name]
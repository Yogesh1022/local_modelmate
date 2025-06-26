# backend/services/database.py

from dotenv import load_dotenv
import os
from motor.motor_asyncio import AsyncIOMotorClient

# ✅ Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", ".env"))

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

if not MONGO_URI or not MONGO_DB_NAME:
    raise RuntimeError("MONGO_URI or MONGO_DB_NAME not found in .env")

# ✅ Async MongoDB client using Motor
client = AsyncIOMotorClient(MONGO_URI)
db = client[MONGO_DB_NAME]

# Optional debug print
print("✅ Connected to MongoDB:", db.name)

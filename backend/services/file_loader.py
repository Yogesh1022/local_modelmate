# backend/services/file_loader.py

import os
import json
from motor.motor_asyncio import AsyncIOMotorClient
from backend.config import settings
from backend.models.history import HistoryModel

client = AsyncIOMotorClient(settings.MONGO_URI)
db = client[settings.MONGO_DB_NAME]

DATASET_PATH = os.path.abspath(os.path.join("data", "academic_projects.json"))

def load_dataset():
    try:
        with open(DATASET_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            print("❌ Dataset is not a list of projects.")
            return []
        return data
    except Exception as e:
        print(f"❌ Failed to load dataset: {e}")
        return []

def find_project_by_prompt(prompt: str, diagram_type: str):
    prompt = prompt.lower().strip()
    for project in load_dataset():
        if prompt in project.get("project_name", "").lower():
            if diagram_type in project:
                return project
    return None

# ✅ Save history to MongoDB
async def save_history(user_id: str, prompt: str, diagram_type: str, source: str = "dataset"):
    history = HistoryModel(
        user_id=user_id,
        prompt=prompt,
        diagram_type=diagram_type,
        source=source
    )
    await db["history"].insert_one(history.dict())

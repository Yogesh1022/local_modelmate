from fastapi import APIRouter, Depends, HTTPException
from pymongo import DESCENDING
from backend.services.auth_service import get_current_user
from backend.services.file_loader import db
from backend.models.history import HistoryModel

router = APIRouter(tags=["User History"])

@router.get("/", response_model=list[HistoryModel], summary="Get user diagram generation history")
async def get_history(user=Depends(get_current_user)):
    try:
        print("📥 Fetching history for user:", user["_id"])
        
        cursor = db["history"].find({"user_id": user["_id"]}).sort("timestamp", DESCENDING)
        raw_results = await cursor.to_list(length=10)

        print(f"📦 Found {len(raw_results)} history records.")
        return [HistoryModel(**item) for item in raw_results]

    except Exception as e:
        print("🔥 History Fetch Error:", e)
        raise HTTPException(status_code=500, detail=f"Error fetching history: {str(e)}")

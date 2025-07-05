import logging
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from pymongo import DESCENDING
from pymongo.errors import ConnectionFailure, OperationFailure
from backend.services.auth_service import get_current_user

from backend.models.user import UserOut
from backend.models.history import HistoryModel

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("history.log")
    ]
)
logger = logging.getLogger(__name__)

# Constants
HISTORY_COLLECTION = "history"

router = APIRouter(
    prefix="/history",
    tags=["User History"],
    responses={404: {"description": "Not found"}}
)

@router.get(
    "/",
    response_model=List[HistoryModel],
    summary="Get user diagram generation history",
    status_code=status.HTTP_200_OK
)
async def get_history(
    user: UserOut = Depends(get_current_user),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Maximum number of records to return")
) -> List[HistoryModel]:
    """
    Retrieve the diagram generation history for the authenticated user.
    Results are sorted by timestamp in descending order.
    """
    logger.info(f"Fetching history for user: {user.email} (skip={skip}, limit={limit})")

    try:
        # Access MongoDB collection
        collection = db[HISTORY_COLLECTION]

        # Query history with pagination
        cursor = collection.find({"user_id": str(user.id)}).sort("timestamp", DESCENDING).skip(skip).limit(limit)
        raw_results = await cursor.to_list(length=limit)

        # Convert to HistoryModel
        try:
            results = [HistoryModel(**item) for item in raw_results]
            logger.info(f"Found {len(results)} history records for user {user.email}")
            return results
        except ValueError as ve:
            logger.error(f"Invalid history data for user {user.email}: {str(ve)}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid history data format"
            )

    except ConnectionFailure as cf:
        logger.error(f"MongoDB connection error: {str(cf)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed"
        )
    except OperationFailure as of:
        logger.error(f"MongoDB operation failed: {str(of)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database operation failed"
        )
    except Exception as e:
        logger.error(f"Error fetching history for user {user.email}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error fetching history"
        )
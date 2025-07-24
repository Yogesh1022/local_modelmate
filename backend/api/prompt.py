from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import Any, Dict
import logging

from backend.services.auth_service import get_current_user
from backend.services.prompt_service import process_prompt, get_prompt_history

router = APIRouter(
    prefix="/prompt",
    tags=["Prompt"]
)

logger = logging.getLogger(__name__)

class PromptRequest(BaseModel):
    prompt: str

@router.post("/process")
async def process_prompt_endpoint(
    request: PromptRequest,
    current_user: Any = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Process a prompt request. Requires authentication.
    """
    try:
        result = await process_prompt(request.prompt, current_user)
        return {"success": True, "result": result}
    except Exception as e:
        logger.error(f"Error processing prompt: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process prompt"
        )

@router.get("/history")
async def prompt_history_endpoint(
    limit: int = 10,
    current_user: Any = Depends(get_current_user)
) -> Dict[str, Any]:
    """
    Get prompt history for the authenticated user.
    """
    try:
        history = await get_prompt_history(current_user, limit)
        return {"success": True, "history": history}
    except Exception as e:
        logger.error(f"Error fetching prompt history: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch prompt history"
        )

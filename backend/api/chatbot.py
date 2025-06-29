import logging
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from backend.services.llm_router import call_together_ai

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("chatbot.log")
    ]
)
logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/chatbot",
    tags=["Chatbot"],
    responses={404: {"description": "Not found"}}
)

class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="User's input message to the chatbot"
    )
    model_config = {"extra": "forbid"}

class ChatResponse(BaseModel):
    response: str = Field(
        ...,
        description="Chatbot's response to the user's message"
    )

@router.post("/", response_model=ChatResponse, status_code=status.HTTP_200_OK)
@router.post("/chatbot/", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def chat_with_bot(request_data: ChatRequest) -> ChatResponse:
    """Process a user message and return a chatbot response."""
    logger.info(f"Received chatbot message: {request_data.message[:50]}...")

    if not request_data.message.strip():
        logger.warning("Empty message received")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Empty message."
        )

    try:
        system_prompt = "You are a helpful assistant chatbot for software engineering students."
        reply = await call_together_ai(
            system_prompt=system_prompt,
            user_input=request_data.message
        )
        logger.info("Chatbot response generated successfully")
        return ChatResponse(response=reply)
    except ValueError as ve:
        logger.error(f"Invalid input to Together AI: {str(ve)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid input: {str(ve)}"
        )
    except Exception as e:
        logger.error(f"Chatbot error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing the chatbot request."
        )
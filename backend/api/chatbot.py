from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.services.llm_router import call_together_ai

router = APIRouter(tags=["Chatbot"])

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
@router.post("/", response_model=ChatResponse)
async def chat_with_bot(request_data: ChatRequest):
    print("📥 Received chatbot message:", request_data.message)

    if not request_data.message.strip():
        raise HTTPException(status_code=400, detail="Empty message.")

    try:
        system_prompt = "You are a helpful assistant chatbot for software engineering students."
        reply = call_together_ai(system_prompt=system_prompt, user_input=request_data.message)
        return ChatResponse(response=reply)
    except Exception as e:
        print("🔥 Chatbot route error:", str(e))
        raise HTTPException(status_code=500, detail=f"Chatbot failed: {str(e)}")

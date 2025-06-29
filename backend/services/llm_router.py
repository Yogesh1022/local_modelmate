import logging
from typing import List, Dict, Any
from together import Together
from fastapi import HTTPException, status
from fastapi.concurrency import run_in_threadpool
from backend.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("llm_router.log")
    ]
)
logger = logging.getLogger(__name__)

class TogetherClient:
    def __init__(self):
        self.api_key = settings.TOGETHER_API_KEY
        self.model = "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"
        if not self.api_key:
            logger.error("TOGETHER_API_KEY is not set in environment")
            raise ValueError("TOGETHER_API_KEY must be set in environment")
        self.client = Together(api_key=self.api_key)

    async def chat(self, messages: List[Dict[str, Any]], temperature: float = 0.7, max_tokens: int = 512) -> str:
        """
        Send a chat request to Together AI and return the response.

        Args:
            messages: List of message dictionaries with role and content.
            temperature: Controls randomness of the response (default: 0.7).
            max_tokens: Maximum number of tokens in the response (default: 512).

        Returns:
            The generated response string.

        Raises:
            HTTPException: For API errors or invalid responses.
        """
        logger.info(f"Sending request to Together AI with model: {self.model}")
        try:
            # Use run_in_threadpool to call the sync SDK method
            response = await run_in_threadpool(
                self.client.chat.completions.create,
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            logger.info("Received response from Together AI")
            if hasattr(response, "choices") and response.choices and hasattr(response.choices[0], "message"):
                return response.choices[0].message.content
            else:
                logger.error("Unexpected response format from Together AI")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Unexpected response format from Together AI"
                )
        except Exception as e:
            logger.error(f"Error from Together AI: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to generate response from Together AI: {str(e)}"
            )

async def call_together_ai(system_prompt: str, user_input: str) -> str:
    """
    Reusable helper to call Together AI with a system prompt and user input.

    Args:
        system_prompt: The system prompt to guide the AI.
        user_input: The user's input query.

    Returns:
        The AI-generated response string.
    """
    if not system_prompt or not user_input:
        logger.warning("Empty system prompt or user input")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="System prompt and user input are required"
        )
    client = TogetherClient()
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]
    return await client.chat(messages)
# Local test for debugging
if __name__ == "__main__":
    import asyncio
    async def test():
        try:
            reply = await call_together_ai(
                system_prompt="You are a helpful assistant that generates PlantUML class diagrams.",
                user_input="Generate a class diagram for a Hospital Management System"
            )
            logger.info(f"Together AI response: {reply}")
            print(f"🤖 Together AI says:\n{reply}")
        except Exception as e:
            logger.error(f"Test error: {str(e)}")
            print(f"❌ Test error: {str(e)}")
    asyncio.run(test())
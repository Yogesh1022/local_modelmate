# backend/services/llm_router.py

import requests
from backend.config import settings

class TogetherClient:
    def __init__(self):
        self.api_key = settings.TOGETHER_API_KEY
        self.base_url = "https://api.together.xyz/v1/chat/completions"
        self.model = "mistralai/Mixtral-8x7B-Instruct-v0.1"

        if not self.api_key:
            raise ValueError("❌ TOGETHER_API_KEY is not set in environment")

    def chat(self, messages: list[dict], temperature: float = 0.7, max_tokens: int = 512) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        try:
            print("📡 Sending request to Together.AI...")  # Log outgoing request
            response = requests.post(self.base_url, headers=headers, json=payload)
            response.raise_for_status()
            result = response.json()

            print("✅ Together.AI raw response:", result)  # Log full response

            if (
                "choices" in result
                and len(result["choices"]) > 0
                and "message" in result["choices"][0]
                and "content" in result["choices"][0]["message"]
            ):
                return result["choices"][0]["message"]["content"]
            else:
                print("⚠️ Unexpected response format:", result)
                return "❌ Response format error from Together.AI"

        except requests.exceptions.RequestException as e:
            print("❌ HTTP error from Together.AI:", e)
        except Exception as e:
            print("❌ Unexpected error:", e)

        return "Sorry, I couldn’t generate a response at the moment."


# 🧠 Reusable helper
def call_together_ai(system_prompt: str, user_input: str) -> str:
    client = TogetherClient()
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_input}
    ]
    return client.chat(messages)


# ✅ Local test for debugging
if __name__ == "__main__":
    reply = call_together_ai(
        system_prompt="You are a helpful assistant that generates PlantUML class diagrams.",
        user_input="Generate a class diagram for a Hospital Management System"
    )
    print("🤖 Together.AI says:\n", reply)

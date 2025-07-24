# Setup and Installation Guide for Llama Model "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free" with Together Client

This guide explains how to properly set up and use the Llama model "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free" via the Together client in this backend project.

---

## 1. Install Dependencies

Ensure you have Python 3.8+ installed.

Install the Together SDK Python package:

```bash
pip install together
```

Also, install FastAPI and other dependencies if not already installed:

```bash
pip install fastapi uvicorn pydantic python-dotenv
```

---

## 2. Configure Environment Variables

Create a `.env` file in the `backend/` directory (or set environment variables in your system) with the following:

```
TOGETHER_API_KEY=your_together_ai_api_key_here
```

Replace `your_together_ai_api_key_here` with your actual Together.AI API key.

---

## 3. Configuration in `backend/config.py`

The configuration file `backend/config.py` contains the following relevant settings:

```python
TOGETHER_API_KEY: str  # Loaded from environment variable
LLM_DEFAULT_MODEL: str = "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"
LLM_DEFAULT_TEMPERATURE: float = 0.7
LLM_DEFAULT_MAX_TOKENS: int = 1024
```

Make sure these are set correctly. The API key is loaded from the environment, and the model name is set as above.

---

## 4. Usage in Code

- `backend/services/llm_router.py` contains the `TogetherClient` class which initializes the Together client with the API key and model.
- Use the async method `chat(messages, temperature, max_tokens)` to send chat completions requests.
- The helper function `call_together_ai(system_prompt, user_input, **kwargs)` wraps the client usage for convenience.
- `backend/services/together_generator.py` shows an example usage of `call_together_ai` to generate PlantUML diagrams.

---

## 5. Running Locally

You can test the Together client integration by running the test block in `backend/services/llm_router.py`:

```bash
cd backend
python -m backend.services.llm_router
```

This will run a local async test sending a prompt to Together.AI and print the response.

---

## 6. Notes

- Ensure your environment has internet access to reach Together.AI API.
- Handle exceptions as shown in the code to manage API errors gracefully.
- Adjust temperature and max_tokens parameters as needed for your use case.

---

This setup should enable you to use the Llama model via Together.AI in your backend services.

If you need further assistance or code improvements, please let me know.

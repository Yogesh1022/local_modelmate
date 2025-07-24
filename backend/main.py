# # from fastapi import FastAPI, HTTPException, Depends, Request
# # from fastapi.security import OAuth2PasswordBearer
# # from fastapi.middleware.cors import CORSMiddleware
# # from fastapi.responses import JSONResponse
# # from fastapi.exceptions import RequestValidationError
# # from starlette.exceptions import HTTPException as StarletteHTTPException
# # from pydantic import BaseModel
# # import logging
# # import sys
# # import os
# # from typing import Dict, Any, List, Optional
# # from contextlib import asynccontextmanager
# # from dotenv import load_dotenv
# # from backend.services.auth_service import LoginRequest  # ✅ full path from project root



# # oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# # # Import services
# # from backend.services.auth_service import (
# #     create_user, verify_user_otp, create_access_token, get_current_user, authenticate_user
# # )
# # from backend.services.database import get_db, initialize_database
# # from backend.services.prompt_service import (
# #     process_user_prompt, get_user_prompt_history, delete_prompt_result
# # )
# # from backend.config import settings

# # # Load environment variables
# # load_dotenv()

# # # Configure logging
# # logging.basicConfig(
# #     level=logging.INFO,
# #     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
# #     handlers=[
# #         logging.StreamHandler(sys.stdout),
# #         logging.FileHandler("modelmate.log")
# #     ]
# # )
# # logger = logging.getLogger(__name__)

# # # Import routers
# # try:
# #     from backend.api import auth, diagram, history, chatbot, research
# #     logger.info("Successfully imported all routers")
# # except ImportError as e:
# #     logger.error(f"Failed to import routers: {str(e)}", exc_info=True)
# #     # Continue without routers for now

# # # Define lifespan for startup and shutdown
# # @asynccontextmanager
# # async def lifespan(app: FastAPI):
# #     logger.info("Starting ModelMate API...")
# #     try:
# #         await initialize_database()
# #         logger.info("Registered routes:")
# #         for route in app.routes:
# #             methods = ", ".join(sorted(route.methods)) if route.methods else "GET"
# #             logger.info(f"  {route.path} ({methods})")
# #         yield
# #     finally:
# #         logger.info("Shutting down ModelMate API...")

# # # Initialize FastAPI app
# # app = FastAPI(
# #     title="ModelMate API",
# #     description="Your Ultimate Guide to Software Modeling with AI",
# #     version="1.0.0",
# #     lifespan=lifespan,
# #     docs_url="/docs",
# #     redoc_url="/redoc",
# #     openapi_url="/openapi.json"
# # )

# # # CORS Middleware
# # app.add_middleware(
# #     CORSMiddleware,
# #     allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5173,http://localhost:8080").split(","), # I've added your frontend's default port 5173
# #     allow_credentials=True,
# #     allow_methods=["*"],
# #     allow_headers=["*"],
# # )

# # # Generic OPTIONS handler for CORS preflight requests
# # # from fastapi import Response

# # # @app.options("/{rest_of_path:path}")
# # # async def options_handler(rest_of_path: str):
# # #     return Response(status_code=204)


# # # Pydantic models for request/response
# # class PromptRequest(BaseModel):
# #     prompt: str
# #     prompt_type: Optional[str] = "general"

# # class PromptResponse(BaseModel):
# #     source: str
# #     data: str
# #     timestamp: str
# #     prompt_type: str
# #     cached: bool

# # # Exception Handlers
# # @app.exception_handler(StarletteHTTPException)
# # async def http_exception_handler(request, exc):
# #     logger.error(f"HTTP error occurred: {exc.detail} for {request.url}")
# #     return JSONResponse(
# #         status_code=exc.status_code,
# #         content={"message": exc.detail}
# #     )

# # @app.exception_handler(RequestValidationError)
# # async def validation_exception_handler(request, exc):
# #     logger.error(f"Validation error for {request.url}: {exc.errors()}")
# #     return JSONResponse(
# #         status_code=422,
# #         content={"message": "Validation error", "details": exc.errors()}
# #     )

# # @app.exception_handler(Exception)
# # async def general_exception_handler(request, exc):
# #     logger.error(f"Unexpected error for {request.url}: {str(exc)}", exc_info=True)
# #     return JSONResponse(
# #         status_code=500,
# #         content={"message": "Internal server error"}
# #     )

# # # Prompt processing endpoints
# # @app.post("/api/prompt/process", response_model=PromptResponse)
# # async def handle_prompt_request(
# #     request: PromptRequest,
# #     current_user: Dict = Depends(get_current_user)
# # ):
# #     logger.info(f"Processing prompt request from user: {current_user['email']}")
# #     if not request.prompt.strip():
# #         raise HTTPException(status_code=400, detail="Prompt cannot be empty")
# #     try:
# #         result = await process_user_prompt(
# #             prompt=request.prompt,
# #             user_id=current_user["_id"],
# #             prompt_type=request.prompt_type
# #         )
# #         return PromptResponse(**result)
# #     except Exception as e:
# #         logger.error(f"Prompt processing error: {str(e)}")
# #         raise HTTPException(status_code=500, detail="Prompt processing failed")

# # @app.get("/api/prompt/history")
# # async def get_prompt_history(
# #     limit: int = 10,
# #     current_user: Dict = Depends(get_current_user)
# # ):
# #     try:
# #         history = await get_user_prompt_history(current_user["_id"], limit)
# #         return {"history": history}
# #     except Exception as e:
# #         logger.error(f"Failed to retrieve prompt history: {str(e)}")
# #         raise HTTPException(status_code=500, detail="Failed to retrieve history")

# # @app.delete("/api/prompt/{prompt_hash}")
# # async def delete_prompt(
# #     prompt_hash: str,
# #     current_user: Dict = Depends(get_current_user)
# # ):
# #     try:
# #         success = await delete_prompt_result(current_user["_id"], prompt_hash)
# #         if success:
# #             return {"message": "Prompt result deleted successfully"}
# #         else:
# #             raise HTTPException(status_code=404, detail="Prompt result not found")
# #     except HTTPException:
# #         raise
# #     except Exception as e:
# #         logger.error(f"Failed to delete prompt result: {str(e)}")
# #         raise HTTPException(status_code=500, detail="Failed to delete prompt result")

# # # Auth Endpoints (Fallback if auth router is not implemented)
# # import random
# # import smtplib
# # from email.mime.text import MIMEText
# # from email.mime.multipart import MIMEMultipart
# # from datetime import datetime

# # def send_email(to_email: str, subject: str, body: str):
# #     sender_email = os.getenv("EMAIL_USER")
# #     sender_password = os.getenv("EMAIL_PASS")
# #     smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
# #     smtp_port = int(os.getenv("SMTP_PORT", "465"))
# #     if not all([sender_email, sender_password, smtp_server, smtp_port]):
# #         logger.error("SMTP configuration is incomplete. Cannot send email.")
# #         return False
# #     message = MIMEMultipart()
# #     message["From"] = sender_email
# #     message["To"] = to_email
# #     message["Subject"] = subject
# #     message.attach(MIMEText(body, "plain"))
# #     try:
# #         with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
# #             server.login(sender_email, sender_password)
# #             server.sendmail(sender_email, to_email, message.as_string())
# #         logger.info(f"Email sent to {to_email}")
# #         return True
# #     except Exception as e:
# #         logger.error(f"Failed to send email to {to_email}: {str(e)}")
# #         return False

# # # @app.post("/auth/signup")
# # # async def signup(name: str, email: str, password: str):
# # #     logger.info(f"Signup attempt for email: {email}")
# # #     user = await create_user(name, email, password)
# # #     if not user:
# # #         raise HTTPException(status_code=400, detail="Email already exists")
# # #     otp = f"{random.randint(100000, 999999)}"
# # #     logger.info(f"Generated OTP for {email}: {otp}")
# # #     from backend.services.database import get_otp_collection
# # #     otp_collection = await get_otp_collection()
# # #     await otp_collection.insert_one({
# # #         "email": email.lower().strip(),
# # #         "otp": otp,
# # #         "created_at": datetime.utcnow()
# # #     })
# # #     subject = "Your OTP Code"
# # #     body = f"Your OTP code is: {otp}"
# # #     email_sent = send_email(email, subject, body)
# # #     if not email_sent:
# # #         return {"success": False, "message": "Failed to send OTP email. Please try again later."}
# # #     return {"success": True, "message": "OTP sent to your email. Please verify to complete signup."}

# # # In main.py

# # @app.post("/auth/signup")
# # async def signup(name: str, email: str, password: str):
# #     logger.info(f"Signup attempt for email: {email}")

# #     # The create_user function returns (None, None) if the user exists
# #     user, otp = await create_user(name, email, password)

# #     if not user:
# #         # This is the crucial check to prevent re-registration
# #         raise HTTPException(status_code=400, detail="Email already registered. Please log in.")

# #     # The rest of the logic only runs for new users
# #     logger.info(f"Generated OTP for {email}: {otp}")
    
# #     subject = "Your OTP Code"
# #     body = f"Your OTP code is: {otp}"
    
# #     email_sent = send_email(email, subject, body)
    
# #     if not email_sent:
# #         # You might want to delete the user here or have a cleanup process
# #         # For now, we'll just inform the client.
# #         raise HTTPException(status_code=500, detail="Failed to send OTP email. Please try again later.")
        
# #     return {"success": True, "message": "OTP sent to your email. Please verify to complete signup."}
# # @app.post("/auth/verify-otp")
# # async def verify_otp(email: str, otp: str):
# #     logger.info(f"OTP verification attempt for email: {email}")
# #     if await verify_user_otp(email, otp):
# #         db = await get_db()
# #         user = await db[settings.USERS_COLLECTION].find_one({"email": email.lower().strip()})
# #         if user:
# #             user["_id"] = str(user["_id"])
# #             token = create_access_token(user["_id"])
# #             return {"success": True, "message": "Signup successful.", "token": token}
# #         raise HTTPException(status_code=400, detail="User not found")
# #     raise HTTPException(status_code=400, detail="Invalid OTP")

# # # from pydantic import BaseModel

# # # class LoginRequest(BaseModel):
# # #     email: str
# # #     password: str

# # @app.post("/auth/login")
# # async def login(data: LoginRequest):
# #     email = data.email
# #     password = data.password
# #     logger.info(f"Login attempt for email: {email}")
# #     user = await authenticate_user(email, password)
# #     if not user:
# #         logger.warning(f"Login failed for email: {email}")
# #         raise HTTPException(status_code=401, detail="Invalid email or password")
# #     token = create_access_token(user["_id"])
# #     logger.info(f"Login successful for email: {email}")
# #     response = JSONResponse(content={
# #         "success": True,
# #         "token": token,
# #         "user": {"_id": user["_id"], "email": user["email"], "name": user["name"]}
# #     })
# #     response.set_cookie(
# #         key="access_token",
# #         value=token,
# #         httponly=True,
# #         samesite="lax",
# #         secure=False  # Set to True if using HTTPS
# #     )
# #     return response

# # # Include API routers if available
# # try:
# #     app.include_router(diagram.router, tags=["Diagram"])
# #     app.include_router(history.router, prefix="/history", tags=["History"])
# #     app.include_router(chatbot.router, prefix="/chatbot", tags=["Chatbot"])
# #     app.include_router(research.router, prefix="/research", tags=["Research"])
# #     logger.info("All routers included successfully")
# # except Exception as e:
# #     logger.warning(f"Some routers not available: {str(e)}")

# # # Health Check Routes
# # @app.get("/", response_model=Dict[str, str])
# # async def read_root() -> Dict[str, str]:
# #     logger.info("Health check endpoint accessed")
# #     return {"message": "🚀 ModelMate Backend is running!"}

# # @app.get("/health")
# # async def health_check():
# #     return {
# #         "status": "healthy",
# #         "version": "1.0.0",
# #         "database": "MongoDB",
# #         "llm_provider": "Together.ai",
# #         "features": [
# #             "prompt_processing",
# #             "intelligent_caching",
# #             "user_authentication",
# #             "project_planning"
# #         ]
# #     }

# # if __name__ == "__main__":
# #     import uvicorn
# #     uvicorn.run(
# #         app,
# #         host=os.getenv("HOST", "0.0.0.0"),
# #         port=int(os.getenv("PORT", 8000)),
# #         log_level="info",
# #         workers=int(os.getenv("WORKERS", 1))
# #     )


# # new updated code

# from fastapi import FastAPI, HTTPException, Depends
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import JSONResponse
# from fastapi.exceptions import RequestValidationError
# from starlette.exceptions import HTTPException as StarletteHTTPException
# from pydantic import BaseModel
# import logging
# import sys
# import os
# from typing import Dict, Any, Optional
# from contextlib import asynccontextmanager
# from dotenv import load_dotenv
# import random
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from datetime import datetime

# # Import services and settings
# from backend.services.auth_service import (
#     create_user, verify_user_otp, create_access_token, get_current_user, authenticate_user
# )
# from backend.services.database import get_db, initialize_database
# from backend.services.prompt_service import (
#     process_user_prompt, get_user_prompt_history, delete_prompt_result
# )
# from backend.config import settings

# # Load environment variables
# load_dotenv()

# # Configure logging
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
#     handlers=[
#         logging.StreamHandler(sys.stdout),
#         logging.FileHandler("modelmate.log")
#     ]
# )
# logger = logging.getLogger(__name__)

# # Define lifespan for startup and shutdown
# @asynccontextmanager
# async def lifespan(app: FastAPI):
#     logger.info("Starting ModelMate API...")
#     await initialize_database()
#     yield
#     logger.info("Shutting down ModelMate API...")

# # Initialize FastAPI app
# app = FastAPI(
#     title="ModelMate API",
#     description="Your Ultimate Guide to Software Modeling with AI",
#     version="1.0.0",
#     lifespan=lifespan,
#     docs_url="/docs",
#     redoc_url="/redoc",
# )

# # CORS Middleware Setup
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5173,http://localhost:8080").split(","),
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # --- Pydantic Models for Request/Response Validation ---

# class SignupRequest(BaseModel):
#     name: str
#     email: str
#     password: str

# class LoginRequest(BaseModel):
#     email: str
#     password: str

# class VerifyOtpRequest(BaseModel):
#     email: str
#     otp: str

# class PromptRequest(BaseModel):
#     prompt: str
#     prompt_type: Optional[str] = "general"

# class PromptResponse(BaseModel):
#     source: str
#     data: str
#     timestamp: str
#     prompt_type: str
#     cached: bool

# # --- Exception Handlers ---

# @app.exception_handler(StarletteHTTPException)
# async def http_exception_handler(request, exc):
#     logger.error(f"HTTP error: {exc.detail} for {request.url}")
#     return JSONResponse(status_code=exc.status_code, content={"message": exc.detail})

# @app.exception_handler(RequestValidationError)
# async def validation_exception_handler(request, exc):
#     logger.error(f"Validation error for {request.url}: {exc.errors()}")
#     return JSONResponse(status_code=422, content={"message": "Validation error", "details": exc.errors()})

# @app.exception_handler(Exception)
# async def general_exception_handler(request, exc):
#     logger.error(f"Unexpected error for {request.url}: {str(exc)}", exc_info=True)
#     return JSONResponse(status_code=500, content={"message": "Internal server error"})


# # --- Authentication Endpoints ---

# def send_email(to_email: str, subject: str, body: str):
#     # This function remains the same
#     sender_email = os.getenv("EMAIL_USER")
#     sender_password = os.getenv("EMAIL_PASS")
#     smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
#     smtp_port = int(os.getenv("SMTP_PORT", "465"))
#     if not all([sender_email, sender_password, smtp_server, smtp_port]):
#         logger.error("SMTP configuration is incomplete. Cannot send email.")
#         return False
#     message = MIMEMultipart()
#     message["From"] = sender_email
#     message["To"] = to_email
#     message["Subject"] = subject
#     message.attach(MIMEText(body, "plain"))
#     try:
#         with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
#             server.login(sender_email, sender_password)
#             server.sendmail(sender_email, to_email, message.as_string())
#         logger.info(f"Email sent to {to_email}")
#         return True
#     except Exception as e:
#         logger.error(f"Failed to send email to {to_email}: {str(e)}")
#         return False

# @app.post("/auth/signup")
# async def signup(data: SignupRequest):  # ✅ FIX: Use Pydantic model to receive JSON body
#     logger.info(f"Signup attempt for email: {data.email}")

#     # The create_user function from auth_service handles the logic
#     # of checking for existing users and creating new ones.
#     user, otp = await create_user(data.name, data.email, data.password)

#     if not user:
#         # This means the email already exists, as handled in auth_service.py
#         raise HTTPException(status_code=400, detail="Email already registered. Please log in.")

#     # The rest of the logic only runs for new users
#     logger.info(f"Generated OTP for {data.email}: {otp}")
    
#     subject = "Your ModelMate OTP Code"
#     body = f"Your OTP code is: {otp}"
    
#     email_sent = send_email(data.email, subject, body)
    
#     if not email_sent:
#         raise HTTPException(status_code=500, detail="Failed to send OTP email. Please try again later.")
        
#     return {"success": True, "message": "OTP sent to your email. Please verify to complete signup."}

# @app.post("/auth/verify-otp")
# async def verify_otp(data: VerifyOtpRequest): # ✅ FIX: Use Pydantic model for consistency
#     logger.info(f"OTP verification attempt for email: {data.email}")
#     if await verify_user_otp(data.email, data.otp):
#         db = await get_db()
#         user = await db[settings.USERS_COLLECTION].find_one({"email": data.email.lower().strip()})
#         if user:
#             user["_id"] = str(user["_id"])
#             token = create_access_token(user["_id"])
#             return {"success": True, "message": "Signup successful.", "token": token}
#         raise HTTPException(status_code=400, detail="User not found after OTP verification.")
#     raise HTTPException(status_code=400, detail="Invalid OTP.")

# @app.post("/auth/login")
# async def login(data: LoginRequest):
#     logger.info(f"Login attempt for email: {data.email}")
#     user = await authenticate_user(data.email, data.password)
#     if not user:
#         logger.warning(f"Login failed for email: {data.email}")
#         raise HTTPException(status_code=401, detail="Invalid email or password")
    
#     token = create_access_token(user["_id"])
#     logger.info(f"Login successful for email: {data.email}")
    
#     response = JSONResponse(content={
#         "success": True,
#         "token": token,
#         "user": {"_id": user["_id"], "email": user["email"], "name": user["name"]}
#     })
#     response.set_cookie(
#         key="access_token",
#         value=token,
#         httponly=True,
#         samesite="lax",
#         secure=False,  # Set True in production with HTTPS
#     )
#     return response

# # --- Main Application Endpoints ---

# @app.post("/api/prompt/process", response_model=PromptResponse)
# async def handle_prompt_request(request: PromptRequest, current_user: Dict = Depends(get_current_user)):
#     logger.info(f"Processing prompt request from user: {current_user['email']}")
#     if not request.prompt.strip():
#         raise HTTPException(status_code=400, detail="Prompt cannot be empty")
#     try:
#         result = await process_user_prompt(
#             prompt=request.prompt,
#             user_id=current_user["_id"],
#             prompt_type=request.prompt_type
#         )
#         # Ensure the returned dict matches the PromptResponse model
#         return result
#     except Exception as e:
#         logger.error(f"Prompt processing error: {str(e)}")
#         raise HTTPException(status_code=500, detail="Prompt processing failed")


# @app.get("/api/prompt/history")
# async def get_prompt_history(limit: int = 10, current_user: Dict = Depends(get_current_user)):
#     try:
#         history = await get_user_prompt_history(current_user["_id"], limit)
#         return {"history": history}
#     except Exception as e:
#         logger.error(f"Failed to retrieve prompt history: {str(e)}")
#         raise HTTPException(status_code=500, detail="Failed to retrieve history")

# @app.delete("/api/prompt/{prompt_hash}")
# async def delete_prompt(prompt_hash: str, current_user: Dict = Depends(get_current_user)):
#     try:
#         success = await delete_prompt_result(current_user["_id"], prompt_hash)
#         if success:
#             return {"message": "Prompt result deleted successfully"}
#         else:
#             raise HTTPException(status_code=404, detail="Prompt result not found")
#     except HTTPException:
#         raise
#     except Exception as e:
#         logger.error(f"Failed to delete prompt result: {str(e)}")
#         raise HTTPException(status_code=500, detail="Failed to delete prompt result")


# # --- Health Check Routes ---

# @app.get("/", response_model=Dict[str, str])
# async def read_root() -> Dict[str, str]:
#     logger.info("Health check endpoint accessed")
#     return {"message": "🚀 ModelMate Backend is running!"}

# @app.get("/health")
# async def health_check():
#     return {
#         "status": "healthy",
#         "version": "1.0.0",
#         "database": "MongoDB",
#         "llm_provider": "Together.ai",
#     }

# # This allows running the app directly with `python main.py`
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(
#         "main:app",
#         host=os.getenv("HOST", "0.0.0.0"),
#         port=int(os.getenv("PORT", 8000)),
#         log_level="info",
#         reload=True
#     )


from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from pydantic import BaseModel
import logging
import sys
import os
from typing import Dict, Any, List, Optional
from contextlib import asynccontextmanager
from dotenv import load_dotenv

# Import services and settings
from backend.services.auth_service import get_current_user
from backend.services.database import initialize_database
from backend.services.prompt_service import (
    process_user_prompt, get_user_prompt_history, delete_prompt_result
)
# Import all the routers from your api directory
from backend.api import auth, diagram, history, chatbot, research

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("modelmate.log")
    ]
)
logger = logging.getLogger(__name__)

# Define lifespan for startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting ModelMate API...")
    await initialize_database()
    yield
    logger.info("Shutting down ModelMate API...")

# Initialize FastAPI app
app = FastAPI(
    title="ModelMate API",
    description="Your Ultimate Guide to Software Modeling with AI",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Middleware Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5173,http://localhost:8080").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Pydantic Models for Request/Response Validation ---

class PromptRequest(BaseModel):
    prompt: str
    prompt_type: Optional[str] = "general"

class PromptResponse(BaseModel):
    source: str
    data: str
    timestamp: str
    prompt_type: str
    cached: bool

# --- Exception Handlers ---

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    logger.error(f"HTTP error: {exc.detail} for {request.url}")
    return JSONResponse(status_code=exc.status_code, content={"message": exc.detail})

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    logger.error(f"Validation error for {request.url}: {exc.errors()}")
    return JSONResponse(status_code=422, content={"message": "Validation error", "details": exc.errors()})

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unexpected error for {request.url}: {str(exc)}", exc_info=True)
    return JSONResponse(status_code=500, content={"message": "Internal server error"})

# --- Main Application Endpoints ---

@app.post("/api/prompt/process", response_model=PromptResponse)
async def handle_prompt_request(request: PromptRequest, current_user: Dict = Depends(get_current_user)):
    logger.info(f"Processing prompt request from user: {current_user['email']}")
    if not request.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    try:
        result = await process_user_prompt(
            prompt=request.prompt,
            user_id=current_user["_id"],
            prompt_type=request.prompt_type
        )
        return result
    except Exception as e:
        logger.error(f"Prompt processing error: {str(e)}")
        raise HTTPException(status_code=500, detail="Prompt processing failed")

@app.get("/api/prompt/history")
async def get_prompt_history(limit: int = 10, current_user: Dict = Depends(get_current_user)):
    try:
        history = await get_user_prompt_history(current_user["_id"], limit)
        return {"history": history}
    except Exception as e:
        logger.error(f"Failed to retrieve prompt history: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve history")

@app.delete("/api/prompt/{prompt_hash}")
async def delete_prompt(prompt_hash: str, current_user: Dict = Depends(get_current_user)):
    try:
        success = await delete_prompt_result(current_user["_id"], prompt_hash)
        if success:
            return {"message": "Prompt result deleted successfully"}
        else:
            raise HTTPException(status_code=404, detail="Prompt result not found")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete prompt result: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to delete prompt result")


# --- Include API Routers ---
# This is the single source of truth for your routes now.
app.include_router(auth.router)
app.include_router(diagram.router, tags=["Diagram"])
app.include_router(history.router, prefix="/history", tags=["History"])
app.include_router(chatbot.router, prefix="/chatbot", tags=["Chatbot"])
app.include_router(research.router, prefix="/research", tags=["Research"])
logger.info("All API routers included successfully.")


# --- Health Check Routes ---

@app.get("/", response_model=Dict[str, str])
async def read_root() -> Dict[str, str]:
    logger.info("Health check endpoint accessed")
    return {"message": "🚀 ModelMate Backend is running!"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "database": "MongoDB",
        "llm_provider": "Together.ai",
    }

# This allows running the app directly with `python main.py` for development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        log_level="info",
        reload=True
    )

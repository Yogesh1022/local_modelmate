from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging
import sys
import os
from typing import Dict, Any, List
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from backend.api import auth, diagram, history, chatbot, research
from backend.api import diagram

from backend.services.auth_service import create_user, verify_user_otp, create_access_token
from backend.services.database import get_db
from backend.config import settings

# Load environment variables
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

# Import routers
try:
    from backend.api import auth, diagram, history, chatbot, research
    logger.info("Successfully imported all routers")
except ImportError as e:
    logger.error(f"Failed to import routers: {str(e)}", exc_info=True)
    raise

# Define lifespan for startup and shutdown
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting ModelMate API...")
    try:
        # Log registered routes for debugging
        logger.info("Registered routes:")
        for route in app.routes:
            methods = ", ".join(sorted(route.methods)) if route.methods else "GET"
            logger.info(f"  {route.path} ({methods})")
        yield
    finally:
        # Shutdown
        logger.info("Shutting down ModelMate API...")

# Initialize FastAPI app
app = FastAPI(
    title="ModelMate API",
    description="Your Ultimate Guide to Software Modeling",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "http://localhost:8000").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception Handlers
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    logger.error(f"HTTP error occurred: {exc.detail} for {request.url}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    logger.error(f"Validation error for {request.url}: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={"message": "Validation error", "details": exc.errors()}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"Unexpected error for {request.url}: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error"}
    )

# Auth Endpoints (Fallback if auth router is not implemented)
@app.post("/auth/signup")
async def signup(name: str, email: str, password: str):
    logger.info(f"Signup attempt for email: {email}")
    user, otp = await create_user(name, email, password)
    if not user:
        raise HTTPException(status_code=400, detail="Email already exists")
    # Simulate OTP sending (replace with email service like SendGrid)
    logger.info(f"OTP for {email}: {otp}")
    return {"success": True, "message": "OTP sent to your email."}

@app.post("/auth/verify-otp")
async def verify_otp(email: str, otp: str):
    logger.info(f"OTP verification attempt for email: {email}")
    if await verify_user_otp(email, otp):
        db = await get_db()
        user = await db[settings.USERS_COLLECTION].find_one({"email": email.lower().strip()})
        if user:
            user["_id"] = str(user["_id"])
            token = create_access_token(user["_id"])
            return {"success": True, "message": "Signup successful.", "token": token}
        raise HTTPException(status_code=400, detail="User not found")
    raise HTTPException(status_code=400, detail="Invalid OTP")

# API Routers
try:
    from backend.api import auth as auth_router
    app.include_router(auth_router.router, prefix="/auth", tags=["Auth"])
    app.include_router(diagram.router, tags=["Diagram"])
    app.include_router(history.router, prefix="/history", tags=["History"])
    app.include_router(chatbot.router, prefix="/chatbot", tags=["Chatbot"])
    app.include_router(research.router, prefix="/research", tags=["Research"])
    logger.info("All routers included successfully")
except Exception as e:
    logger.error(f"Failed to include routers: {str(e)}", exc_info=True)
    raise

# Health Check Route
@app.get("/", response_model=Dict[str, str])
async def read_root() -> Dict[str, str]:
    logger.info("Health check endpoint accessed")
    return {"message": "🚀 ModelMate Backend is running!"}

# Extended Health Check to Verify Endpoints
@app.get("/health", response_model=Dict[str, List[str]])
async def health_check() -> Dict[str, List[str]]:
    """Return a list of registered endpoints for debugging."""
    logger.info("Health check endpoint accessed")
    routes = []
    for route in app.routes:
        methods = ", ".join(sorted(route.methods)) if route.methods else "GET"
        routes.append(f"{route.path} ({methods})")
    return {"endpoints": routes}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=os.getenv("HOST", "0.0.0.0"),
        port=int(os.getenv("PORT", 8000)),
        log_level="info",
        workers=int(os.getenv("WORKERS", 1))
    )
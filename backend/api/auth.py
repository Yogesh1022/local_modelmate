from fastapi import APIRouter, Request, HTTPException, Depends, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field
from typing import Any, Dict
from datetime import datetime
import logging

from backend.models.user import UserOut
from backend.services.auth_service import (
    create_user,
    authenticate_user,
    create_access_token,
    verify_user_otp,
    get_current_user,
)
from backend.config import settings

router = APIRouter(
    tags=["Authentication"],
    responses={404: {"description": "Not found"}},
    prefix="/auth"
)

logger = logging.getLogger(__name__)

# Basic placeholder for Google OAuth route
@router.get("/google")
async def google_oauth_redirect(request: Request):
    """
    Redirect to Google OAuth login page.
    This is a placeholder implementation.
    """
    # Replace the URL below with your actual Google OAuth URL
    google_oauth_url = "https://accounts.google.com/o/oauth2/auth?client_id=YOUR_CLIENT_ID&redirect_uri=YOUR_REDIRECT_URI&response_type=code&scope=email profile"
    logger.info("Redirecting to Google OAuth")
    return RedirectResponse(url=google_oauth_url)

class SignupRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="User's full name")
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=8, description="User's password")

    class Config:
        extra = "forbid"  # For Pydantic v1
    # For Pydantic v2:
    # model_config = {"extra": "forbid"}

class TokenResponse(BaseModel):
    access_token: str = Field(..., description="JWT access token")
    token_type: str = Field(default="bearer", description="Token type")
    user: UserOut = Field(..., description="User details")

class SignupResponse(BaseModel):
    success: bool = Field(..., description="Whether the signup was successful")
    message: str = Field(..., description="Status message")

class VerifyOtpResponse(SignupResponse):
    token: str = Field(..., description="JWT access token if verification succeeds")

def clean_user_data(user: Dict[str, Any]) -> Dict[str, Any]:
    try:
        user_clean = user.copy()
        created_at = user_clean.get("created_at")
        if isinstance(created_at, str):
            try:
                user_clean["created_at"] = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
            except ValueError as e:
                logger.error(f"Invalid datetime format for created_at: {str(e)}")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Invalid user data format"
                )
        return user_clean
    except Exception as e:
        logger.error(f"Error cleaning user data: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing user data"
        )

@router.post("/signup", response_model=SignupResponse, status_code=status.HTTP_201_CREATED)
async def signup(data: SignupRequest) -> SignupResponse:
    logger.info(f"Attempting to sign up user with email: {data.email}")
    try:
        user, otp = await create_user(data.name, data.email, data.password)
        if not user:
            logger.warning(f"Signup failed: User with email {data.email} already exists")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already exists"
            )

        # Simulate OTP sending (replace with email service like SendGrid)
        logger.info(f"OTP for {data.email}: {otp}")
        return SignupResponse(
            success=True,
            message="OTP sent to your email."
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Signup error for {data.email}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating user"
        )

@router.post("/verify-otp", response_model=VerifyOtpResponse)
async def verify_otp(email: EmailStr, otp: str) -> VerifyOtpResponse:
    logger.info(f"Attempting OTP verification for email: {email}")
    try:
        if await verify_user_otp(email, otp):
            from backend.services.database import get_db
            db = await get_db()
            user = await db[settings.USERS_COLLECTION].find_one({"email": email.lower().strip()})
            if user:
                user["_id"] = str(user["_id"])
                token = create_access_token(user["_id"])
                return VerifyOtpResponse(
                    success=True,
                    message="Signup successful.",
                    token=token
                )
            raise HTTPException(status_code=400, detail="User not found")
        raise HTTPException(status_code=400, detail="Invalid OTP")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"OTP verification error for {email}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error verifying OTP"
        )

@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> TokenResponse:
    logger.info(f"Attempting login for user: {form_data.username}")
    try:
        user = await authenticate_user(form_data.username, form_data.password)
        if not user:
            logger.warning(f"Login failed for {form_data.username}: Invalid credentials")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"}
            )

        token = create_access_token(str(user["_id"]))
        user_clean = clean_user_data(user)

        logger.info(f"User {form_data.username} logged in successfully")
        return TokenResponse(
            access_token=token,
            token_type="bearer",
            user=UserOut(**user_clean)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error for {form_data.username}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error during authentication"
        )

@router.get("/me", response_model=UserOut)
async def get_logged_in_user(current_user: UserOut = Depends(get_current_user)) -> UserOut:
    logger.info(f"Fetching details for user: {current_user.email}")
    try:
        return current_user
    except Exception as e:
        logger.error(f"Error fetching user details: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving user data"
        )

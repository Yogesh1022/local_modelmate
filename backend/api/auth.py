import logging
from typing import Any, Dict
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field
from backend.services.auth_service import (
    create_user,
    authenticate_user,
    create_access_token,
    get_current_user,
)
from backend.models.user import UserOut
from backend.config import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("auth.log")
    ]
)
logger = logging.getLogger(__name__)

router = APIRouter(
    tags=["Authentication"],
    responses={404: {"description": "Not found"}}
)

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

@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def signup(data: SignupRequest) -> TokenResponse:
    logger.info(f"Attempting to sign up user with email: {data.email}")
    try:
        user = await create_user(data.name, data.email, data.password)
        if not user:
            logger.warning(f"Signup failed: User with email {data.email} already exists")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User already exists"
            )

        token = create_access_token(str(user["_id"]))
        user_clean = clean_user_data(user)

        logger.info(f"User {data.email} signed up successfully")
        return TokenResponse(
            access_token=token,
            token_type="bearer",
            user=UserOut(**user_clean)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Signup error for {data.email}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating user"
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

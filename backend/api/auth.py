from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
from backend.services.auth_service import (
    create_user,
    authenticate_user,
    create_access_token,
    get_current_user,
)
from backend.models.user import UserOut
from datetime import datetime
from typing import Any  # ✅ FIXED

router = APIRouter(tags=["Authentication"])



class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


@router.post("/signup", response_model=TokenResponse)
async def signup(data: SignupRequest):
    user = await create_user(data.name, data.email, data.password)
    if not user:
        raise HTTPException(status_code=400, detail="User already exists")

    token = create_access_token(user["_id"])

    user_clean: dict[str, Any] = user.copy()  # ✅ FIXED
    if isinstance(user_clean.get("created_at"), str):
        user_clean["created_at"] = datetime.fromisoformat(user_clean["created_at"].replace("Z", ""))

    return {
        "access_token": token,
        "user": UserOut(**user_clean),
    }


@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(user["_id"])

    user_clean: dict[str, Any] = user.copy()  # ✅ FIXED
    if isinstance(user_clean.get("created_at"), str):
        user_clean["created_at"] = datetime.fromisoformat(user_clean["created_at"].replace("Z", ""))

    return {
        "access_token": token,
        "user": UserOut(**user_clean),
    }


@router.get("/me", response_model=UserOut)
async def get_logged_in_user(current_user=Depends(get_current_user)):
    return current_user

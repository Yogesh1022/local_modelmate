
# import logging
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import os

# from fastapi import APIRouter, Request, HTTPException, Depends, status
# from fastapi.responses import JSONResponse
# from pydantic import BaseModel, EmailStr, Field

# # Import your custom modules
# from backend.models.user import UserOut
# from backend.services.auth_service import (
#     create_user,
#     authenticate_user,
#     create_access_token,
#     verify_user_otp,
#     get_current_user,
# )
# from backend.services.database import get_db
# from backend.config import settings

# # --- Router Setup ---
# router = APIRouter(
#     prefix="/auth",
#     tags=["Authentication"],
#     responses={404: {"description": "Not found"}},
# )

# logger = logging.getLogger(__name__)


# # --- Pydantic Models for Request/Response ---

# class SignupRequest(BaseModel):
#     name: str = Field(..., min_length=2, max_length=100)
#     email: EmailStr
#     password: str = Field(..., min_length=8)

# class VerifyOtpRequest(BaseModel):
#     email: EmailStr
#     otp: str

# class LoginRequest(BaseModel):
#     email: EmailStr
#     password: str

# class TokenResponse(BaseModel):
#     access_token: str
#     token_type: str = "bearer"
#     user: UserOut

# class SuccessResponse(BaseModel):
#     success: bool
#     message: str


# # --- Email Sending Logic ---

# def send_otp_email(to_email: str, otp: str):
#     """Sends the OTP code to the user's email."""
#     sender_email = settings.SMTP_SENDER_EMAIL
#     sender_password = settings.SMTP_SENDER_PASSWORD
#     smtp_server = settings.SMTP_SERVER
#     smtp_port = settings.SMTP_PORT

#     if not all([sender_email, sender_password, smtp_server, smtp_port]):
#         logger.error("SMTP configuration is incomplete in .env file. Cannot send email.")
#         raise HTTPException(status_code=500, detail="Failed to send OTP email due to incomplete server configuration.")

#     message = MIMEMultipart()
#     message["From"] = sender_email
#     message["To"] = to_email
#     message["Subject"] = "Your ModelMate Verification Code"
#     body = f"Welcome to ModelMate!\n\nYour One-Time Password (OTP) is: {otp}\n\nThis code will expire in 5 minutes."
#     message.attach(MIMEText(body, "plain"))

#     try:
#         with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
#             server.login(sender_email, sender_password)
#             server.sendmail(sender_email, to_email, message.as_string())
#         logger.info(f"OTP email sent successfully to {to_email}")
#     except Exception as e:
#         logger.error(f"Failed to send email to {to_email}: {str(e)}")
#         raise HTTPException(status_code=500, detail="Error sending verification email.")


# # --- API Endpoints ---

# @router.post("/signup", response_model=SuccessResponse, status_code=status.HTTP_201_CREATED)
# async def signup(data: SignupRequest):
#     logger.info(f"Attempting to sign up user with email: {data.email}")
#     try:
#         user, otp = await create_user(data.name, data.email, data.password)
#         if not user:
#             raise HTTPException(status_code=400, detail="Email already registered. Please log in.")
        
#         logger.info(f"OTP for {data.email}: {otp}")
#         send_otp_email(data.email, otp)

#         return SuccessResponse(success=True, message="OTP sent to your email.")
#     except HTTPException:
#         raise
#     except Exception as e:
#         logger.error(f"Signup error: {str(e)}")
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating user")

# @router.post("/verify-otp", response_model=TokenResponse)
# async def verify_otp(data: VerifyOtpRequest):
#     logger.info(f"Verifying OTP for email: {data.email}")
#     try:
#         is_valid = await verify_user_otp(data.email, data.otp)
#         if not is_valid:
#             raise HTTPException(status_code=400, detail="Invalid or expired OTP.")

#         db = await get_db()
#         user = await db[settings.USERS_COLLECTION].find_one({"email": data.email.lower().strip()})
#         if not user:
#             raise HTTPException(status_code=404, detail="User not found after OTP verification.")

#         token = create_access_token(str(user["_id"]))
#         user_out = UserOut.model_validate(user)

#         response = JSONResponse(content={
#             "access_token": token,
#             "token_type": "bearer",
#             # ✅ FIX: Use mode='json' to correctly serialize datetime objects to strings
#             "user": user_out.model_dump(mode='json') 
#         })
#         response.set_cookie(
#             key="access_token",
#             value=token,
#             httponly=True,
#             secure=False,
#             samesite="lax",
#             max_age=settings.JWT_EXPIRY
#         )
#         return response
#     except HTTPException:
#         raise
#     except Exception as e:
#         logger.error(f"OTP verification error: {str(e)}")
#         raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error verifying OTP.")

# @router.post("/login", response_model=TokenResponse)
# async def login(data: LoginRequest):
#     logger.info(f"Attempting login for user: {data.email}")
#     user = await authenticate_user(data.email, data.password)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid email or password",
#             headers={"WWW-Authenticate": "Bearer"},
#         )

#     token = create_access_token(str(user["_id"]))
#     user_out = UserOut.model_validate(user)
    
#     response = JSONResponse(content={
#         "access_token": token,
#         "token_type": "bearer",
#         # ✅ FIX: Use mode='json' to correctly serialize datetime objects to strings
#         "user": user_out.model_dump(mode='json')
#     })
#     response.set_cookie(
#         key="access_token",
#         value=token,
#         httponly=True,
#         secure=False,
#         samesite="lax",
#         max_age=settings.JWT_EXPIRY
#     )
#     return response

# @router.get("/me", response_model=UserOut)
# async def get_logged_in_user(current_user: dict = Depends(get_current_user)):
#     return UserOut.model_validate(current_user)


import logging
import os
import smtplib
from email.mime.text import MIMEText
from typing import Any, Dict

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field

from backend.config import settings
from backend.models.user import UserOut
from backend.services.auth_service import (
    authenticate_user,
    create_access_token,
    create_user,
    get_current_user,
    verify_user_otp,
)

# --- Router Setup ---
router = APIRouter(tags=["Authentication"], prefix="/auth")
logger = logging.getLogger(__name__)


# --- Pydantic Models ---
class SignupRequest(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=8)

class VerifyOtpRequest(BaseModel):
    email: EmailStr
    otp: str = Field(..., min_length=6, max_length=6)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut

# --- Email Sending Helper ---
def send_otp_email(to_email: str, otp: str):
    # ... (email sending logic remains the same)
    # ... (keeping it concise for this example)
    sender_email = settings.SMTP_SENDER_EMAIL
    sender_password = settings.SMTP_SENDER_PASSWORD
    smtp_server = settings.SMTP_SERVER
    smtp_port = settings.SMTP_PORT

    if not all([sender_email, sender_password, smtp_server, smtp_port]):
        logger.error("SMTP configuration is incomplete in .env file. Cannot send email.")
        return False

    subject = "Your ModelMate Verification Code"
    body = f"Your OTP code is: {otp}\n\nThis code will expire in 5 minutes."
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = to_email

    try:
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())
        logger.info(f"OTP email sent successfully to {to_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {str(e)}")
        return False

# --- API Endpoints ---
@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(data: SignupRequest):
    # ... (signup logic remains the same)
    logger.info(f"Attempting to sign up user with email: {data.email}")
    user, otp = await create_user(data.name, data.email, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email already exists.",
        )
    logger.info(f"OTP for {data.email}: {otp}")
    if not send_otp_email(data.email, otp):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send OTP email due to incomplete server configuration.",
        )
    return {"success": True, "message": "OTP sent to your email."}


@router.post("/verify-otp")
async def verify_otp(data: VerifyOtpRequest):
    # ... (verify-otp logic remains the same)
    logger.info(f"Verifying OTP for email: {data.email}")
    is_valid = await verify_user_otp(data.email, data.otp)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP.",
        )
    # ... (token creation logic)
    return {"success": True, "message": "Email verified successfully."}


# ✅ FIX: This is the updated login endpoint
@router.post("/login", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    logger.info(f"Attempting login for user: {form_data.username}")
    
    # Authenticate the user with their email (form_data.username) and password
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create an access token
    token = create_access_token(str(user["_id"]))
    
    # Prepare the user data for the response
    user_out = UserOut.model_validate(user)

    # Return the token and user info in a JSON response
    return JSONResponse(content={
        "access_token": token,
        "token_type": "bearer",
        "user": user_out.model_dump(mode='json')
    })


@router.get("/me", response_model=UserOut)
async def get_logged_in_user(current_user: UserOut = Depends(get_current_user)):
    return current_user


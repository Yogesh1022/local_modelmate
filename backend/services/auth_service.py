# backend/services/auth_service.py

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from backend.services.database import db
from bson import ObjectId  # ✅ Needed for _id queries
import os

# JWT config
SECRET_KEY = os.getenv("JWT_SECRET", "supersecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECONDS = int(os.getenv("JWT_EXPIRY", 3600))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ---------- Helper Functions ----------
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(user_id: str):
    expire = datetime.utcnow() + timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONDS)
    to_encode = {"sub": user_id, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ---------- MongoDB-based Auth ----------
async def create_user(name: str, email: str, password: str):
    existing = await db.users.find_one({"email": email})
    if existing:
        return None
    user = {
        "name": name,
        "email": email,
        "hashed_password": get_password_hash(password),
        "created_at": datetime.utcnow()
    }
    result = await db.users.insert_one(user)
    user["_id"] = str(result.inserted_id)
    return user

async def authenticate_user(email: str, password: str):
    user = await db.users.find_one({"email": email})
    if not user or not verify_password(password, user["hashed_password"]):
        return None
    user["_id"] = str(user["_id"])
    return user

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = await db.users.find_one({"_id": ObjectId(user_id)})
        if user:
            user["_id"] = str(user["_id"])
            return user
        raise HTTPException(status_code=401, detail="User not found")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

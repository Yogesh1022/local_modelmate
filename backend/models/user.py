from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


class User(BaseModel):
    name: str = Field(..., description="Full name of the user")
    email: EmailStr = Field(..., description="Email address (used as unique ID)")
    password: str = Field(..., description="Hashed password")
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


# ✅ Add this class to fix the "UserOut" import issue
class UserOut(BaseModel):
    name: str
    email: EmailStr
    created_at: Optional[datetime]

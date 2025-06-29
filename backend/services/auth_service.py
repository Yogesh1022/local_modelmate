from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from backend.services.database import get_collection
from bson import ObjectId
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("logs/auth_service.log")
    ]
)
logger = logging.getLogger(__name__)

# JWT config from environment
from backend.config import settings
SECRET_KEY = settings.JWT_SECRET
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECONDS = settings.JWT_EXPIRY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Cache MongoDB collection
_users_collection = None

async def get_users_collection():
    """
    Get or initialize the MongoDB users collection with index creation.
    """
    global _users_collection
    if _users_collection is None:
        _users_collection = await get_collection(settings.USERS_COLLECTION)
        try:
            indexes = await _users_collection.index_information()
            if "email_1" not in indexes:
                logger.info("Creating unique index on email field")
                await _users_collection.create_index([("email", 1)], unique=True, name="email_1")
                logger.info("Unique index on email created successfully")
            else:
                logger.info("Unique index on email already exists")
        except Exception as e:
            logger.error(f"Failed to create index on email: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=500,
                detail=f"Failed to initialize database indexes: {str(e)}"
            )
    return _users_collection

# ---------- Helper Functions ----------
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters")
    return pwd_context.hash(password)

def create_access_token(user_id: str):
    expire = datetime.utcnow() + timedelta(seconds=ACCESS_TOKEN_EXPIRE_SECONDS)
    to_encode = {"sub": user_id, "exp": expire}
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ---------- MongoDB-based Auth ----------
async def create_user(name: str, email: str, password: str):
    logger.info(f"Creating user with email: {email}")
    try:
        collection = await get_users_collection()
        existing = await collection.find_one({"email": email.lower().strip()})
        if existing:
            logger.warning(f"User with email {email} already exists")
            return None

        user = {
            "name": name.strip(),
            "email": email.lower().strip(),
            "hashed_password": get_password_hash(password),
            "created_at": datetime.utcnow()
        }
        logger.info(f"Attempting to insert user: {user}")
        result = await collection.insert_one(user)
        user["_id"] = str(result.inserted_id)
        logger.info(f"User {email} created successfully with ID: {user['_id']}")
        return user
    except Exception as e:
        logger.error(f"Error creating user {email}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error creating user")

async def authenticate_user(email: str, password: str):
    logger.info(f"Authenticating user: {email}")
    try:
        collection = await get_users_collection()
        user = await collection.find_one({"email": email.lower().strip()})
        if not user or not verify_password(password, user["hashed_password"]):
            logger.warning(f"Authentication failed for {email}: Invalid credentials")
            return None
        user["_id"] = str(user["_id"])
        logger.info(f"User {email} authenticated successfully")
        return user
    except Exception as e:
        logger.error(f"Error authenticating user {email}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error during authentication")

async def get_current_user(request: Request, token: str = Depends(oauth2_scheme)):
    """
    Get the current user from JWT token in Authorization header or cookie.
    Prefer header, fallback to cookie.
    """
    # Prefer Authorization header, fallback to cookie
    header_token = token
    cookie_token = request.cookies.get("access_token")
    token_to_use = header_token or cookie_token

    if not token_to_use:
        logger.warning("No JWT token found in header or cookie")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"}
        )
    try:
        payload = jwt.decode(token_to_use, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            logger.warning("Invalid token: No user_id in payload")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"}
            )
        collection = await get_users_collection()
        user = await collection.find_one({"_id": ObjectId(user_id)})
        if not user:
            logger.warning(f"User not found for ID: {user_id}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
                headers={"WWW-Authenticate": "Bearer"}
            )
        user["_id"] = str(user["_id"])
        logger.info(f"User retrieved successfully: {user['email']}")
        return user
    except JWTError:
        logger.warning("Invalid or expired token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    except Exception as e:
        logger.error(f"Error retrieving user: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving user data"
        )
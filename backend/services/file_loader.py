import logging
import os
import json
from typing import List, Dict, Any, Optional
from fastapi import HTTPException, status
from backend.config import settings
from backend.services.database import get_collection
from backend.models.history import HistoryModel

from backend.services.database import get_collection

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("file_loader.log")
    ]
)
logger = logging.getLogger(__name__)

# Dataset path
DATASET_PATH = os.path.abspath(os.path.join("data", "academic_projects.json"))

# Cache dataset globally
_dataset_cache = None

def load_dataset() -> List[Dict[str, Any]]:
    """
    Load and cache the academic projects dataset.

    Returns:
        List of project dictionaries.

    Raises:
        HTTPException: If the dataset file is not found or invalid.
    """
    global _dataset_cache
    if _dataset_cache is None:
        try:
            logger.info(f"Loading dataset from {DATASET_PATH}")
            with open(DATASET_PATH, "r", encoding="utf-8") as f:
                _dataset_cache = json.load(f)
            if not isinstance(_dataset_cache, list):
                logger.error("Dataset is not a list of projects")
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Dataset is not a list of projects"
                )
            logger.info(f"Loaded {len(_dataset_cache)} projects from dataset")
        except FileNotFoundError:
            logger.error(f"Dataset file not found: {DATASET_PATH}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Dataset file not found"
            )
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in dataset: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Invalid dataset format"
            )
        except Exception as e:
            logger.error(f"Unexpected error loading dataset: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error loading dataset"
            )
    return _dataset_cache

def find_project_by_prompt(prompt: str, diagram_type: str) -> Optional[Dict[str, Any]]:
    """
    Find a project matching the prompt and diagram type.

    Args:
        prompt: User input prompt.
        diagram_type: Type of diagram (class, sequence, usecase).

    Returns:
        Matching project dictionary or None if no match is found.
    """
    logger.info(f"Searching for project with prompt: {prompt[:50]}... and diagram_type: {diagram_type}")
    prompt = prompt.lower().strip()
    for project in load_dataset():
        if not isinstance(project, dict):
            logger.warning("Skipping invalid project entry: not a dictionary")
            continue
        project_name = project.get("project_name", "").lower()
        if prompt in project_name and diagram_type in project:
            logger.info(f"Found matching project: {project_name}")
            return project
    logger.info("No matching project found")
    return None

async def save_history(user_id: str, prompt: str, diagram_type: str, source: str = "dataset") -> None:
    """
    Save history to MongoDB.

    Args:
        user_id: User's unique ID.
        prompt: User input prompt.
        diagram_type: Type of diagram.
        source: Source of diagram generation (default: dataset).

    Raises:
        HTTPException: For database errors or invalid input.
    """
    logger.info(f"Saving history for user_id: {user_id}, diagram_type: {diagram_type}")
    try:
        # Validate inputs
        if not user_id or not prompt or not diagram_type:
            logger.warning("Invalid history input: missing required fields")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User ID, prompt, and diagram type are required"
            )
        history = HistoryModel(
            user_id=user_id,
            prompt=prompt[:1000],  # Truncate for safety
            diagram_type=diagram_type,
            source=source
        )
        collection = await get_collection(settings.HISTORY_COLLECTION)
        result = await collection.insert_one(history.dict(by_alias=True))
        logger.info(f"History saved with ID: {result.inserted_id}")
    except ConnectionFailure as cf:
        logger.error(f"MongoDB connection error: {str(cf)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connection failed"
        )
    except NetworkTimeout as nt:
        logger.error(f"MongoDB query timeout: {str(nt)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Database query timed out"
        )
    except OperationFailure as of:
        logger.error(f"MongoDB operation failed: {str(of)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database operation failed"
        )
    except Exception as e:
        logger.error(f"Error saving history: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error saving history"
        )
import logging
from typing import List, Dict, Any
from fastapi import APIRouter, HTTPException, status, Query
from pydantic import BaseModel, Field
import json
import os
from backend.config import settings

# Attempt to import rapidfuzz for optional fuzzy matching
try:
    from rapidfuzz import fuzz
    RAPIDFUZZ_AVAILABLE = True
except ImportError:
    RAPIDFUZZ_AVAILABLE = False
    fuzz = None

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("research.log")
    ]
)
logger = logging.getLogger(__name__)

# Cache dataset globally
_dataset_cache = None

def load_dataset() -> List[Dict[str, Any]]:
    """Load and cache the academic projects dataset."""
    global _dataset_cache
    if _dataset_cache is None:
        dataset_path = settings.DATASET_PATH
        try:
            logger.info(f"Loading dataset from {dataset_path}")
            with open(dataset_path, "r", encoding="utf-8") as f:
                _dataset_cache = json.load(f)
            if not isinstance(_dataset_cache, list):
                logger.error("Dataset is not a list")
                raise ValueError("Dataset must be a list of projects")
            if not _dataset_cache:
                logger.warning("Dataset is empty")
            logger.info(f"Loaded {len(_dataset_cache)} projects from dataset")
        except FileNotFoundError:
            logger.error(f"Dataset file not found: {dataset_path}")
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
    return _dataset_cache

class ProjectResponse(BaseModel):
    project_name: str = Field(..., description="Name of the academic project")
    description: str = Field(default="No description available.", description="Project description")

    model_config = {"extra": "forbid"}

class SearchResponse(BaseModel):
    results: List[ProjectResponse] = Field(..., description="List of matching projects")

router = APIRouter(
    prefix="/research",
    tags=["Research"],
    responses={404: {"description": "Not found"}}
)

def score_project(prompt_tokens: List[str], project: Dict[str, Any], use_fuzzy: bool = False) -> float:
    """Score a project based on relevance to the prompt tokens."""
    name = project.get("project_name", "").lower()
    desc = project.get("description", "").lower()
    score = 0.0

    for token in prompt_tokens:
        if not token:
            continue
        # Exact substring matching
        if token in name:
            score += settings.RESEARCH_NAME_WEIGHT  # Higher weight for project name
        if token in desc:
            score += settings.RESEARCH_DESC_WEIGHT  # Lower weight for description
        # Optional fuzzy matching if rapidfuzz is available and enabled
        if use_fuzzy and RAPIDFUZZ_AVAILABLE:
            name_score = fuzz.partial_ratio(token, name) / 100.0
            desc_score = fuzz.partial_ratio(token, desc) / 100.0
            if name_score >= settings.RESEARCH_FUZZY_THRESHOLD:
                score += name_score * settings.RESEARCH_NAME_WEIGHT
            if desc_score >= settings.RESEARCH_FUZZY_THRESHOLD:
                score += desc_score * settings.RESEARCH_DESC_WEIGHT

    return score

@router.get(
    "/",
    response_model=SearchResponse,
    summary="Search academic projects",
    status_code=status.HTTP_200_OK
)
async def search_research(
    prompt: str = Query(
        ...,
        min_length=2,
        max_length=500,
        description="Search prompt for academic projects"
    )
) -> SearchResponse:
    """
    Search and return the top academic projects matching the given prompt.
    Returns up to a configured number of results, sorted by relevance.

    Args:
        prompt: The search query string.

    Returns:
        A SearchResponse containing a list of matching projects.

    Raises:
        HTTPException: For invalid prompts or dataset errors.
    """
    logger.info(f"Processing search query: {prompt[:50]}...")

    try:
        # Validate and normalize prompt
        prompt_lower = prompt.strip().lower()
        if not prompt_lower:
            logger.warning("Empty prompt after stripping")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Prompt cannot be empty"
            )

        # Split prompt into tokens for better matching
        prompt_tokens = [token.strip() for token in prompt_lower.split() if token.strip()]
        if not prompt_tokens:
            logger.warning("No valid tokens in prompt")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Prompt contains no valid terms"
            )

        # Load dataset
        dataset = load_dataset()

        # Score projects
        scored_projects = []
        use_fuzzy = settings.get("RESEARCH_USE_FUZZY", False)
        if use_fuzzy and not RAPIDFUZZ_AVAILABLE:
            logger.warning("Fuzzy matching enabled but rapidfuzz is not installed; falling back to exact matching")
            use_fuzzy = False
        for project in dataset:
            # Validate project structure
            if "project_name" not in project:
                logger.warning(f"Skipping project with missing project_name: {project}")
                continue
            score = score_project(prompt_tokens, project, use_fuzzy)
            if score > 0:
                scored_projects.append((score, project))

        # Sort and select top results
        max_results = settings.get("RESEARCH_MAX_RESULTS", 5)
        top_projects = sorted(scored_projects, key=lambda x: x[0], reverse=True)[:max_results]
        results = [
            ProjectResponse(
                project_name=proj["project_name"],
                description=proj.get("description", "No description available.")
            )
            for _, proj in top_projects
        ]

        logger.info(f"Found {len(results)} matching projects for prompt: {prompt[:50]}...")
        return SearchResponse(results=results)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Search error for prompt '{prompt[:50]}...': {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error processing search request"
        )
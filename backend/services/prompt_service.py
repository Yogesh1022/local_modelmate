# import logging
# from datetime import datetime
# from typing import Dict, Any, List
# from backend.services.database import get_prompt_results_collection
# from backend.services.llm_router import call_together_ai, hash_prompt
# from backend.config import settings
# from backend.services.file_loader import find_project_by_prompt, load_dataset

# logger = logging.getLogger(__name__)

# async def process_user_prompt(prompt: str, user_id: str, prompt_type: str = "general") -> Dict[str, Any]:
#     """
#     Process user prompt: Check DB first, fetch from LLM if needed, and store results.

#     Args:
#         prompt: The user's input prompt
#         user_id: The authenticated user's ID
#         prompt_type: Type of prompt (general, project_planning, research, etc.)

#     Returns:
#         Dict containing the result data and metadata
#     """
#     collection = await get_prompt_results_collection()
#     prompt_hash = hash_prompt(f"{prompt}_{prompt_type}")

#     logger.info(f"Processing prompt for user {user_id}, hash: {prompt_hash[:10]}...")

#     # Step 1: Check if data exists in DB
#     existing = await collection.find_one({
#         "prompt_hash": prompt_hash, 
#         "user_id": user_id,
#         "prompt_type": prompt_type
#     })

#     if existing:
#         logger.info(f"Cache hit for prompt hash: {prompt_hash[:10]}")
#         return {
#             "source": "database",
#             "data": existing["result"],
#             "timestamp": existing["timestamp"],
#             "prompt_type": existing["prompt_type"],
#             "cached": True,
#             "prompt_hash": prompt_hash
#         }

#     # Step 2: Fetch from LLM if not found
#     try:
#         system_prompt = get_system_prompt_by_type(prompt_type)
#         llm_result = await call_together_ai(system_prompt, prompt)
#         logger.info(f"LLM fetch successful for prompt hash: {prompt_hash[:10]}")
#     except Exception as e:
#         logger.error(f"LLM fetch failed: {str(e)}")
#         raise

#     # Step 3: Store in MongoDB
#     doc = {
#         "user_id": user_id,
#         "prompt": prompt,
#         "prompt_hash": prompt_hash,
#         "prompt_type": prompt_type,
#         "result": llm_result,
#         "timestamp": datetime.utcnow(),
#         "model_used": getattr(settings, "LLM_DEFAULT_MODEL", "unknown"),
#         "cached": False
#     }

#     try:
#         await collection.insert_one(doc)
#         logger.info(f"Stored new result for prompt hash: {prompt_hash[:10]}")
#     except Exception as e:
#         logger.error(f"Failed to store result: {str(e)}")
#         # Don't fail the request if storage fails

#     return {
#         "source": "llm",
#         "data": llm_result,
#         "timestamp": doc["timestamp"],
#         "prompt_type": prompt_type,
#         "cached": False,
#         "prompt_hash": prompt_hash
#     }

# def get_system_prompt_by_type(prompt_type: str) -> str:
#     """
#     Get appropriate system prompt based on the prompt type.
#     """
#     system_prompts = {
#         "general": "You are a helpful assistant that provides detailed and accurate responses.",
#         "project_planning": """You are an expert project planner and software architect. 
#         Generate comprehensive project plans including:
#         - Project scope and objectives
#         - Technical requirements
#         - Implementation phases
#         - Timeline estimates
#         - Risk assessments
#         - Resource requirements
#         Provide detailed, actionable guidance.""",
#         "research": """You are a research assistant specializing in academic and technical research.
#         Help users with:
#         - Research methodology
#         - Literature analysis
#         - Data interpretation
#         - Research planning
#         - Academic writing guidance
#         Provide evidence-based, scholarly responses.""",
#         "diagram": """You are a technical documentation expert specializing in system design.
#         Generate clear technical diagrams and documentation including:
#         - System architecture diagrams
#         - Database schemas
#         - Process workflows
#         - Class diagrams
#         - Sequence diagrams
#         Use appropriate technical notation and best practices.""",
#         "analysis": """You are a data analyst and business intelligence expert.
#         Provide comprehensive analysis including:
#         - Data interpretation
#         - Trend analysis
#         - Performance metrics
#         - Recommendations
#         - Strategic insights
#         Support conclusions with logical reasoning."""
#     }
#     return system_prompts.get(prompt_type, system_prompts["general"])

# async def get_user_prompt_history(user_id: str, limit: int = 10) -> List[dict]:
#     """
#     Retrieve user's prompt history from the database.
#     """
#     collection = await get_prompt_results_collection()
#     try:
#         cursor = collection.find(
#             {"user_id": user_id}
#         ).sort("timestamp", -1).limit(limit)

#         history = []
#         async for doc in cursor:
#             history.append({
#                 "prompt": doc["prompt"],
#                 "prompt_type": doc["prompt_type"],
#                 "timestamp": doc["timestamp"],
#                 "result_preview": doc["result"][:200] + "..." if len(doc["result"]) > 200 else doc["result"],
#                 "prompt_hash": doc.get("prompt_hash")
#             })
#         return history
#     except Exception as e:
#         logger.error(f"Failed to retrieve prompt history: {str(e)}")
#         return []

# async def delete_prompt_result(user_id: str, prompt_hash: str) -> bool:
#     """
#     Delete a specific prompt result from the database.
#     """
#     collection = await get_prompt_results_collection()
#     try:
#         result = await collection.delete_one({
#             "user_id": user_id,
#             "prompt_hash": prompt_hash
#         })
#         return result.deleted_count > 0
#     except Exception as e:
#         logger.error(f"Failed to delete prompt result: {str(e)}")




import logging
from datetime import datetime
from typing import Dict, Any, List

# Added import for local dataset functions
from backend.services.file_loader import find_project_by_prompt, load_dataset

from backend.services.database import get_prompt_results_collection
from backend.services.llm_router import call_together_ai, hash_prompt
from backend.config import settings


logger = logging.getLogger(__name__)


async def process_user_prompt(prompt: str, user_id: str, prompt_type: str = "general") -> Dict[str, Any]:
    """
    Process user prompt: Check local dataset first, then DB cache,
    then fetch from LLM if needed, and store results.

    Args:
        prompt: The user's input prompt
        user_id: The authenticated user's ID
        prompt_type: Type of prompt (general, project_planning, research, etc.)

    Returns:
        Dict containing the result data and metadata
    """
    # Step 1: Check the local academic_projects.json dataset first.
    # This logic assumes that prompts intended for the local dataset will have a
    # specific `prompt_type`, such as "diagram".
    if prompt_type == "diagram":
        load_dataset()  # This is efficient because the dataset is cached in memory
        project = find_project_by_prompt(prompt, prompt_type)
        if project and project.get(prompt_type):
            logger.info(f"Found match in local dataset for prompt: {prompt}")
            return {
                "source": "dataset",
                "data": project[prompt_type],
                "timestamp": datetime.utcnow(),
                "prompt_type": prompt_type,
                "cached": False,  # Not a cached LLM response
                "prompt_hash": hash_prompt(f"{prompt}_{prompt_type}")
            }

    # If not found in local dataset, proceed to check MongoDB cache
    collection = await get_prompt_results_collection()
    prompt_hash = hash_prompt(f"{prompt}_{prompt_type}")

    logger.info(f"Processing prompt for user {user_id}, hash: {prompt_hash[:10]}...")

    # Step 2: Check if data exists in DB (as a cached LLM response)
    existing = await collection.find_one({
        "prompt_hash": prompt_hash,
        "user_id": user_id,
        "prompt_type": prompt_type
    })

    if existing:
        logger.info(f"Cache hit for prompt hash: {prompt_hash[:10]}")
        return {
            "source": "database",
            "data": existing["result"],
            "timestamp": existing["timestamp"].isoformat() if hasattr(existing["timestamp"], "isoformat") else existing["timestamp"],
            "prompt_type": existing["prompt_type"],
            "cached": True,
            "prompt_hash": prompt_hash
        }

    # Step 3: Fetch from LLM if not found in dataset or cache
    try:
        system_prompt = get_system_prompt_by_type(prompt_type)
        llm_result = await call_together_ai(system_prompt, prompt)
        logger.info(f"LLM fetch successful for prompt hash: {prompt_hash[:10]}")
    except Exception as e:
        logger.error(f"LLM fetch failed: {str(e)}")
        raise

    # Step 4: Store in MongoDB
    doc = {
        "user_id": user_id,
        "prompt": prompt,
        "prompt_hash": prompt_hash,
        "prompt_type": prompt_type,
        "result": llm_result,
        "timestamp": datetime.utcnow(),
        "model_used": getattr(settings, "LLM_DEFAULT_MODEL", "unknown"),
        "cached": False
    }

    try:
        await collection.insert_one(doc)
        logger.info(f"Stored new result for prompt hash: {prompt_hash[:10]}")
    except Exception as e:
        logger.error(f"Failed to store result: {str(e)}")
        # Don't fail the request if storage fails

    return {
        "source": "llm",
        "data": llm_result,
        "timestamp": doc["timestamp"].isoformat() if hasattr(doc["timestamp"], "isoformat") else doc["timestamp"],
        "prompt_type": prompt_type,
        "cached": False,
        "prompt_hash": prompt_hash
    }


def get_system_prompt_by_type(prompt_type: str) -> str:
    """
    Get appropriate system prompt based on the prompt type.
    """
    system_prompts = {
        "general": "You are a helpful assistant that provides detailed and accurate responses.",
        "project_planning": """You are an expert project planner and software architect. 
        Generate comprehensive project plans including:
        - Project scope and objectives
        - Technical requirements
        - Implementation phases
        - Timeline estimates
        - Risk assessments
        - Resource requirements
        Provide detailed, actionable guidance.""",
        "research": """You are a research assistant specializing in academic and technical research.
        Help users with:
        - Research methodology
        - Literature analysis
        - Data interpretation
        - Research planning
        - Academic writing guidance
        Provide evidence-based, scholarly responses.""",
        "diagram": """You are a technical documentation expert specializing in system design.
        Generate clear technical diagrams and documentation including:
        - System architecture diagrams
        - Database schemas
        - Process workflows
        - Class diagrams
        - Sequence diagrams
        Use appropriate technical notation and best practices.""",
        "analysis": """You are a data analyst and business intelligence expert.
        Provide comprehensive analysis including:
        - Data interpretation
        - Trend analysis
        - Performance metrics
        - Recommendations
        - Strategic insights
        Support conclusions with logical reasoning."""
    }
    return system_prompts.get(prompt_type, system_prompts["general"])


async def get_user_prompt_history(user_id: str, limit: int = 10) -> List[dict]:
    """
    Retrieve user's prompt history from the database.
    """
    collection = await get_prompt_results_collection()
    try:
        cursor = collection.find(
            {"user_id": user_id}
        ).sort("timestamp", -1).limit(limit)

        history = []
        async for doc in cursor:
            history.append({
                "prompt": doc["prompt"],
                "prompt_type": doc["prompt_type"],
                "timestamp": doc["timestamp"],
                "result_preview": doc["result"][:200] + "..." if len(doc["result"]) > 200 else doc["result"],
                "prompt_hash": doc.get("prompt_hash")
            })
        return history
    except Exception as e:
        logger.error(f"Failed to retrieve prompt history: {str(e)}")
        return []


async def delete_prompt_result(user_id: str, prompt_hash: str) -> bool:
    """
    Delete a specific prompt result from the database.
    """
    collection = await get_prompt_results_collection()
    try:
        result = await collection.delete_one({
            "user_id": user_id,
            "prompt_hash": prompt_hash
        })
        return result.deleted_count > 0
    except Exception as e:
        logger.error(f"Failed to delete prompt result: {str(e)}")
        return False

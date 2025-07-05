import logging
import os
import uuid
import base64
from typing import Dict, Any, Literal
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from backend.services.auth_service import get_current_user
from backend.services.file_loader import (
    load_dataset,
    find_project_by_prompt,
    save_history,
)
from backend.utils.renderer import render_plantuml_to_png
from backend.modules.class_diagram.generator import generate_class_plantuml
from backend.modules.sequence_diagram.generator import generate_sequence_plantuml
from backend.modules.usecase_diagram.generator import generate_usecase_plantuml
from backend.services.together_generator import generate_using_together_ai
from backend.config import settings
from backend.models.user import UserOut

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("diagram.log")
    ]
)
logger = logging.getLogger(__name__)

# Cache dataset globally to avoid reloading
_dataset_cache = None

def get_dataset() -> Dict[str, Any]:
    """Load dataset once and cache it."""
    global _dataset_cache
    if _dataset_cache is None:
        try:
            logger.info("Loading dataset...")
            _dataset_cache = load_dataset()
            logger.info(f"Loaded {len(_dataset_cache)} projects from dataset")
        except Exception as e:
            logger.error(f"Failed to load dataset: {str(e)}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to load dataset"
            )
    return _dataset_cache

router = APIRouter(
    prefix="/diagram",
    tags=["Diagram Generation"],
    responses={404: {"description": "Not found"}}
)

# Request Models
class DiagramRequest(BaseModel):
    prompt: str = Field(
        ...,
        min_length=1,
        max_length=1000,
        description="User prompt for diagram generation"
    )
    diagram_type: Literal["class", "sequence", "usecase"] = Field(
        ...,
        description="Type of diagram to generate"
    )

    model_config = {"extra": "forbid"}

class RenderRequest(BaseModel):
    plantuml: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="PlantUML code to render as PNG"
    )

    model_config = {"extra": "forbid"}

# ...existing code...

async def generate_plantuml_code(project: Dict[str, Any], diagram_type: str, prompt: str) -> tuple[str, str]:
    """Generate PlantUML code based on diagram type and source."""
    try:
        if project:
            logger.info(f"Generating {diagram_type} diagram from dataset")
            if diagram_type == "class":
                plantuml_code = generate_class_plantuml(project["class_diagram"])
            elif diagram_type == "sequence":
                plantuml_code = generate_sequence_plantuml(project["sequence_diagram"])
            elif diagram_type == "usecase":
                plantuml_code = generate_usecase_plantuml(project["use_case_diagram"])
            source = "dataset"
        else:
            logger.info(f"Generating {diagram_type} diagram using Together.AI")
            # Await the async function here!
            plantuml_code = await generate_using_together_ai(
                prompt=prompt,
                diagram_type=diagram_type
            )
            source = "together_ai"
        return plantuml_code, source
    except ValueError as ve:
        logger.error(f"Invalid input for {diagram_type} diagram: {str(ve)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid diagram generation input"
        )
    except Exception as e:
        logger.error(f"Error generating {diagram_type} diagram: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Diagram generation failed"
        )

# ...rest of your code unchanged...

@router.post("/generate", status_code=status.HTTP_200_OK)
async def generate_diagram(
    data: DiagramRequest,
    user: UserOut = Depends(get_current_user)
) -> Dict[str, str]:
    """Generate a PlantUML diagram based on user prompt and diagram type."""
    logger.info(f"User {user['email']} requested {data.diagram_type} diagram with prompt: {data.prompt[:50]}...")
    try:
        # Normalize prompt
        prompt = data.prompt.strip().lower()
        if not prompt:
            logger.warning("Empty prompt after stripping")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Prompt cannot be empty"
            )

        # Load dataset
        dataset = get_dataset()

        # Find project or use Together.AI
        project = find_project_by_prompt(prompt, data.diagram_type)
        plantuml_code, source = await generate_plantuml_code(project, data.diagram_type, prompt)

        # Save history
        try:
            await save_history(
                user_id=str(user["_id"]),  # Ensure string ID
                prompt=prompt,
                diagram_type=data.diagram_type
            )
            logger.info(f"History saved for user {user['email']}")
        except Exception as e:
            logger.error(f"Failed to save history for user {user.email}: {str(e)}")

        return {
            "plantuml": plantuml_code,
            "source": source
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Diagram generation error for user {user.email}: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Diagram generation failed"
        )

@router.post("/render", summary="Render PlantUML to PNG", status_code=status.HTTP_200_OK)
async def render_diagram_image(data: RenderRequest) -> Dict[str, str]:
    """Render PlantUML code to a base64-encoded PNG image."""
    logger.info("Rendering PlantUML to PNG")

    # Basic PlantUML validation
    if not data.plantuml.strip().startswith("@startuml"):
        logger.warning("Invalid PlantUML code: Missing @startuml")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid PlantUML code: Must start with @startuml"
        )

    temp_dir = settings.get("TEMP_DIR", "temp")  # Configurable temp directory
    output_path = f"{temp_dir}/{uuid.uuid4().hex}.png"

    # Delete the temporary file after use
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        success = await render_plantuml_to_png(data.plantuml, output_path)
        if not success or not os.path.exists(output_path):
            logger.error("Rendering failed: Output file not created")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Rendering failed"
            )

        with open(output_path, "rb") as img_file:
            base64_png = base64.b64encode(img_file.read()).decode("utf-8")

        return {"image_base64": base64_png}
    except ValueError as ve:
        logger.error(f"Invalid PlantUML code: {str(ve)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid PlantUML code"
        )
    except Exception as e:
        logger.error(f"Rendering error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Rendering failed"
        )
    finally:
        if os.path.exists(output_path):
            try:
                os.remove(output_path)
                logger.info(f"Temporary file {output_path} deleted")
            except Exception as e:
                logger.error(f"Failed to delete temporary file {output_path}: {str(e)}")
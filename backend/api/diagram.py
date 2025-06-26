from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Literal
import uuid, os, base64

from backend.services.auth_service import get_current_user
from backend.services.file_loader import (
    load_dataset,
    find_project_by_prompt,
    save_history,  # ✅ Add this back
)
from backend.utils.renderer import render_plantuml_to_png
from backend.modules.class_diagram.generator import generate_class_plantuml
from backend.modules.sequence_diagram.generator import generate_sequence_plantuml
from backend.modules.usecase_diagram.generator import generate_usecase_plantuml
from backend.services.together_generator import generate_using_together_ai

router = APIRouter(tags=["Diagram Generation"])

# ===== Request Models =====
class DiagramRequest(BaseModel):
    prompt: str
    diagram_type: Literal["class", "sequence", "usecase"]

class RenderRequest(BaseModel):
    plantuml: str

# ===== MAIN GENERATE ENDPOINT (WITH AUTH) =====
@router.post("/generate")
async def generate_diagram(
    data: DiagramRequest,
    user=Depends(get_current_user)
):
    try:
        print("📥 Prompt:", data.prompt)
        print("📘 Diagram Type:", data.diagram_type)
        print("👤 User ID:", user["_id"])

        prompt = data.prompt.strip().lower()
        diagram_type = data.diagram_type

        # Dataset logic
        dataset = load_dataset()
        print(f"📚 Loaded {len(dataset)} projects from dataset")

        project = find_project_by_prompt(prompt, diagram_type)
        if project:
            print("✅ Found match in dataset")
            if diagram_type == "class":
                plantuml_code = generate_class_plantuml(project["class_diagram"])
            elif diagram_type == "sequence":
                plantuml_code = generate_sequence_plantuml(project["sequence_diagram"])
            elif diagram_type == "usecase":
                plantuml_code = generate_usecase_plantuml(project["use_case_diagram"])
            source = "dataset"
        else:
            print("⚠️ No match found in dataset — using Together.AI")
            plantuml_code = generate_using_together_ai(prompt, diagram_type)
            source = "together_ai"

        # Save history
        await save_history(user_id=user["_id"], prompt=prompt, diagram_type=diagram_type)
        print("💾 History saved.")

        return {
            "plantuml": plantuml_code,
            "source": source
        }

    except Exception as e:
        print("🔥 Diagram generation error:", str(e))
        raise HTTPException(status_code=500, detail="Diagram generation failed")

@router.post("/render", summary="Render PlantUML to PNG")
async def render_diagram_image(data: RenderRequest):
    try:
        output_path = f"temp/{uuid.uuid4().hex}.png"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        success = render_plantuml_to_png(data.plantuml, output_path)
        if not success or not os.path.exists(output_path):
            raise HTTPException(status_code=500, detail="Rendering failed")

        with open(output_path, "rb") as img_file:
            base64_png = base64.b64encode(img_file.read()).decode("utf-8")

        return {"image_base64": base64_png}

    except Exception as e:
        print("❌ Render failed:", e)
        raise HTTPException(status_code=500, detail=f"Rendering failed: {str(e)}")

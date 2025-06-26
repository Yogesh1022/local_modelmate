from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Diagram(BaseModel):
    user_email: str = Field(..., description="Email of the user")
    prompt: str = Field(..., description="Prompt used for generation")
    diagram_type: str = Field(..., description="Type of diagram (class, sequence, usecase)")
    plantuml_code: str = Field(..., description="Generated PlantUML code")
    image_url: Optional[str] = Field(None, description="URL or path to rendered diagram image")
    source: str = Field(..., description="dataset | together_ai")
    created_at: datetime = Field(default_factory=datetime.utcnow)
from typing import Literal

diagram_type: Literal["class", "sequence", "usecase"]
source: Literal["dataset", "together_ai"]

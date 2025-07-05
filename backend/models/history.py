from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class HistoryModel(BaseModel):
    user_id: str = Field(..., description="User's unique ID")
    prompt: str = Field(..., description="User input prompt for diagram")
    diagram_type: str = Field(..., description="Diagram type: class, sequence, usecase")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Generation time")
    source: Optional[str] = Field(default="dataset", description="Source of diagram generation")
    
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

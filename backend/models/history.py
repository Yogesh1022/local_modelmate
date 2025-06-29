from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional



class HistoryModel(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id", description="MongoDB document ID")
    user_id: str = Field(..., description="User's unique ID")
    prompt: str = Field(..., min_length=1, max_length=1000, description="User input prompt for diagram")
    diagram_type: str = Field(..., description="Diagram type: class, sequence, usecase")
    timestamp: datetime = Field(default_factory=datetime.utcnow, description="Generation time")
    source: Optional[str] = Field(default=None, description="Source of diagram generation (e.g., dataset, together_ai)")

    model_config = {
        "from_attributes": True,  # Updated from orm_mode
        "populate_by_name": True,  # Allow population by field name or alias (_id)
        "extra": "forbid",  # Prevent extra fields
        "json_encoders": {
            datetime: lambda v: v.isoformat()  # Preserve datetime serialization
        }
    }
from pydantic import BaseModel, Field
from typing import Optional


class ResearchPaper(BaseModel):
    title: str = Field(..., description="Title of the research paper")
    authors: Optional[str] = Field(None, description="Author(s) of the paper")
    year: Optional[int] = Field(None, description="Publication year")
    abstract: Optional[str] = Field(None, description="Abstract or summary of the paper")
    link: Optional[str] = Field(None, description="URL to the full paper or source")

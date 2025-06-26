from fastapi import APIRouter, HTTPException, Query
import json
import os

router = APIRouter()

DATASET_PATH = os.path.join("data", "academic_projects.json")

@router.get("/")

def search_research(prompt: str = Query(..., min_length=2)):
    """
    Search and return top 5 most relevant academic projects for the given prompt.
    """

    try:
        with open(DATASET_PATH, "r") as f:
            dataset = json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load dataset: {e}")

    prompt_lower = prompt.lower()
    scored_projects = []

    for project in dataset:
        name = project.get("project_name", "").lower()
        desc = project.get("description", "").lower()

        score = 0
        if prompt_lower in name:
            score += 2
        if prompt_lower in desc:
            score += 1

        if score > 0:
            scored_projects.append((score, project))

    # Sort by score descending and return top 5
    top_projects = sorted(scored_projects, key=lambda x: x[0], reverse=True)[:5]
    result = [
        {
            "project_name": proj["project_name"],
            "description": proj.get("description", "No description available.")
        }
        for _, proj in top_projects
    ]

    return {"results": result}

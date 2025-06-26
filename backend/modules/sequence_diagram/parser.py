import json

def load_all_projects(file_path):
    """
    Loads all projects from a given JSON dataset file.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading sequence diagram dataset: {e}")
        return []

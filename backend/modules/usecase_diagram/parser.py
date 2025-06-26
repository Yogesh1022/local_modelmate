import json

def load_all_projects(file_path):
    """
    Loads a list of projects from the dataset file.
    """
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except Exception as e:
        print(f"❌ Error reading JSON file: {e}")
        return []

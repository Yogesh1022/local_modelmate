import json
import os

def load_all_projects(dataset_path: str) -> list:
    """
    Loads all academic projects from the dataset JSON file.

    Args:
        dataset_path (str): Relative or absolute path to the dataset file.

    Returns:
        list: List of project dictionaries.
    """
    try:
        if not os.path.exists(dataset_path):
            print(f"❌ Dataset not found at {dataset_path}")
            return []

        with open(dataset_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            print("❌ Dataset is not a list of projects.")
            return []

        return data

    except json.JSONDecodeError as e:
        print(f"❌ JSON decode error: {e}")
        return []

    except Exception as e:
        print(f"❌ Failed to load dataset: {e}")
        return []

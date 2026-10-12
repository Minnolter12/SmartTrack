import json
import os
from src.courses import Semester

DATA_FILE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "smarttrack_data.json")

def save_semesters(semesters: list[Semester], filepath: str = DATA_FILE_PATH) -> bool:
    """Save all semesters and their courses to a JSON file."""
    try:
        data = {
            "version": "1.0",
            "semesters": [semester.to_dict() for semester in semesters]
        }
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        print(f"Error saving SmartTrack data: {e}")
        return False

def load_semesters(filepath: str = DATA_FILE_PATH) -> list[Semester]:
    """Load all semesters and their courses from a JSON file."""
    if not os.path.exists(filepath):
        return []

    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        semesters_data = data.get("semesters", [])
        return [Semester.from_dict(sem_dict) for sem_dict in semesters_data]
    except Exception as e:
        print(f"Error loading SmartTrack data: {e}")
        return []

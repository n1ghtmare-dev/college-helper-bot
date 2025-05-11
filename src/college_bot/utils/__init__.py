from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

def check_group(user_id: int) -> bool:
    with open(BASE_DIR / "data/groups.json", "r") as file:
        groups = file.read()


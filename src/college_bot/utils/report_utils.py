from datetime import datetime
from config import settings


def calculate_percentage(students_count: int, group_size: int = 30) -> float:
    return round((students_count / group_size) * 100, 2)

    
from __future__ import annotations
import json
import logging
from pathlib import Path
from typing import Dict, List
from contextlib import contextmanager
from college_bot.services.external_db import ExternalDB

logger = logging.getLogger(__name__)

class GroupsUpdater:
    def __init__(self, db_config: dict[str, str], json_path: Path):
        self.db_config = db_config
        self.json_path = json_path

    @contextmanager
    def get_db_connection(self):
        db = ExternalDB(self.db_config)
        try:
            with db as conn:
                yield conn
        except Exception as e:
            logger.error(f"Database error connection: {e}")
            raise
    
    def get_groups_data(self) -> List[Dict]:
        try:
            with self.get_db_connection() as db:
                return db.query("""
                SELECT first_name, students_count, headmen
                FROM users
                WHERE is_active = 1 
                """)
        except Exception as e:
            logger.error(f"Failed to fetch group: {e}")
            return []
        
    def save_to_json(self, data: Dict) -> bool:
        try:
            with open(self.json_path, 'w', encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.info(f"Successfully saved to {self.json_path}")
            return True
        except (IOError, json.JSONDecodeError) as e:
            logger.error(f"Failed to save JSON: {e}")
            return False
        
    def transform_data(self, raw_data: List[Dict]) -> Dict:
        return {
            item['name']:{
                "Количество": item[""],
                "Старосты": self.headmen_parser(item.get('headmen', '')),
            }
            for item in raw_data
        }

    def headmen_parser(self, headmen_str: str) -> List[str]:
        try:
            return json.loads(headmen_str) if headmen_str else []
        except json.JSONDecodeError:
            logger.warning("Invalid headmen format")
            return []

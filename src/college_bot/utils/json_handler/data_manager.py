import json
import logging
from config import settings
from pathlib import Path
from typing import Dict, List, Any
from services.crud.groups_crud import GroupCrud
from services.external_db import ExternalDB

logger = logging.getLogger(__name__)

class GroupsUpdater:
    def __init__(self, db_config: dict[str, str], json_path: Path = None):
        default_json_path = Path(__file__).resolve().parent.parent.parent.parent.parent / "data/groups.json"
        self.db_config = db_config
        self.json_path = json_path if json_path != None else default_json_path
        self.crud = GroupCrud(ExternalDB(db_config))
    
    def get_groups_data(self) -> List[Dict]:
        try:
            groups = self.crud.get_all_groups()
            schedules = self.crud.get_user_group()

            for group in groups:
                group_name = group["name"]
                group['schedule'] = schedules.get(group_name, [])

            return group
        except Exception as e:
            logger.error(f"Failed to fetch data: {e}")
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
        
    def get_headmen(self, group_id: str) -> List[int]:
        try:
            with open(self.json_path, 'r', encoding='utf-8') as file:
                groups_data: Dict[str, Any] = json.load(file)

            group_data = groups_data.get(group_id, {})
            return group_data.get("Старосты", [])
        
        except FileNotFoundError:
            logger.error(f"Error: file {self.json_path} not found")
            return []
        except json.JSONDecodeError:
            logger.error(f"Error: file {self.json_path} has incorrect JSON")
            return []
        
    def add_headman(self, user_id: int, group_id: str) -> bool:
        try:
            with open(self.json_path, 'r', encoding='utf-8') as file:
                groups_data: Dict[str, Any] = json.load(file)

            if group_id not in groups_data:
                logger.error(f"Group {group_id} not found")
                return False
            
            headmen: List[int] = groups_data[group_id].get("Старосты", [])

            if user_id in headmen:
                logger.info(f"User {user_id} is already a headman in group {group_id}")
                return True
            
            headmen.append(user_id)
            groups_data[group_id]["Старосты"] = headmen

            return self.save_to_json(groups_data)

        except FileNotFoundError:
            logger.error(f"Error: file {self.json_path} not found")
            return False
        except json.JSONDecodeError:
            logger.error(f"Error: file {self.json_path} has incorrect JSON")
            return False
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return False
        return True

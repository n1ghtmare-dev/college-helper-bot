from utils.json_handler.data_manager import JsonDataManager
from config import settings
from services.crud.groups_crud import get_schedule
from datetime import datetime
import logging


logger = logging.getLogger(__name__)

class Tasks:
    def __init__(self):
        self.json_manager = JsonDataManager(settings.DB_CONFIG)

    def update_json_from_db(self):
        date = datetime.now().strftime("%d-%m-%Y")
        schedule = get_schedule(date)

        groups_data = self.json_manager.get_groups_data()

        for item in schedule:
            if item['group_id'] not in groups_data:
                groups_data[item['group_id']] = {
                    "Количество": 0,
                    "Старосты": [],
                    "Расписание": []
                }

            groups_data[item['group_id']]['Расписание'] = [{
                'time': item['time'],
                'teacher_id': item['teacher_id']
            }]
            
        self.json_manager.save_to_json(groups_data)
        
    def json_update(self):
        logger.info("Update groups.json from database - started")
        self.update_json_from_db()
        logger.info("groups.json was successfully updated")


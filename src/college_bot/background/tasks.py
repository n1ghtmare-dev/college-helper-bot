from utils.json_handler.data_manager import JsonDataManager
from config import settings
from services.crud.groups_crud import get_schedule
from datetime import datetime
from core.dispatcher import bot
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

    async def create_report(self):

        all_headmen = self.json_manager.get_all_headmen()
        whole_schedule_data = self.json_manager.get_groups_data()

        for group_id, group_info in whole_schedule_data.items():
            if 'Старосты' in group_info and len(group_info['Старосты']) < 1:
                continue
            else:
                if 'Расписание' in group_info and len(group_info['Расписание']) < 1:
                    continue
                else:
                    for lesson in group_info['Расписание']:
                        print("TIME - ", lesson['time'])
                    # Send msg for 20 min after start lesson
                    # await bot.send_message(group_info['Старосты'][0], 'Report')

            print(group_id, group_info)

        await bot.send_message(5438186408, 'Report')

    def check_time(time: str) -> bool:
        ...


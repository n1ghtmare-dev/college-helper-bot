from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from utils.json_handler.data_manager import GroupsUpdater
from services.crud.groups_crud import get_user_group
from config import settings 
from pathlib import Path



router = Router()
json_manager = GroupsUpdater(settings.DB_CONFIG)


@router.callback_query(F.data == 'become_leader')
async def add_headmen(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_group = get_user_group(user_id)
    group_headmen = json_manager.get_headmen(user_group)

    if len(group_headmen) < 2:
        ...
    else:
        pass
    
    
    # get group by user_id
    # check headmen in group
    # add user in group's headmen

    
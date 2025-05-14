from aiogram import Router, types
from aiogram.filters import Command
from services.external_db import ExternalDB
from config import settings
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.json_handler.data_manager import JsonDataManager
from services.crud.groups_crud import get_user_group
from keyboards.inline import get_leader_kb, get_registration_kb


router = Router()
json_manager = JsonDataManager(settings.DB_CONFIG)


@router.message(Command("start"))
async def start(message: types.Message):
    user_id = message.from_user.id

    group = get_user_group(user_id)

    if len(group) > 0:
        group_id = group[0]['group_id']
        await message.answer(f'Вы зарегистрированы в группе {group_id}.')
        group_headmen = json_manager.get_headmen(group_id)
        
        if user_id in group_headmen:
            await message.answer(f'Вы староста своей группы')
        else:
            if len(group_headmen) < 2:
                await message.answer(
                    f'Вы не являетесь старостой, но в этой группе меньше 2-х старост, у Вас есть возможность зарегистрироваться, как староста.',
                    reply_markup=get_leader_kb())
            else:
                await message.answer('В Вашей группе уже зарегистрированы старосты, вы не можете зарегистрироваться')
    else:
        await message.answer('Вы не зарегистрированы в какой-либо группе....')
        await message.answer('Для дальнейшего использования бота Вам необходимо зарегистрироваться в своей группе через другого бота. Вы можете это сделать по кнопке ниже:', reply_markup=get_registration_kb())




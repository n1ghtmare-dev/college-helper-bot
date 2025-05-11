from aiogram import Router, types
from aiogram.filters import Command


router = Router()

@router.message(Command("start"))
async def start(message: types.Message):
    user_id = message.from_user.id

    check_group = ...
    
    #TODO: Проверка группы



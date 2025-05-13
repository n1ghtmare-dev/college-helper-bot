from aiogram import Router, types
from aiogram.filters import Command
from services.external_db import ExternalDB
from config import settings
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


router = Router()

@router.message(Command("start"))
async def start(message: types.Message):
    user_id = message.from_user.id

    with ExternalDB(settings.DB_CONFIG) as db:
        query = db.query('SELECT group_id, username FROM all_users WHERE id_user = %s AND group_id IS NOT NULL', (user_id,))
    
    # TODO: Get out keyboards into other module
    registration = InlineKeyboardMarkup(
         inline_keyboard=[[
              InlineKeyboardButton(
              text='Зарегистрироваться',
              url='https://t.me/Iubip_assistant_bot',
              )]
    ])

    if len(query) > 0:
        group = query[0]['group_id']
        
        headman = True # TODO: -> check headman in group


        await message.answer(f'Вы зарегистрированы в группе {group}.')

        # TODO: Проверка на старосту в json
    else:
        await message.answer('Вы не зарегистрированы в какой-либо группе....')
        await message.answer('Для дальнейшего использования бота Вам необходимо зарегистрироваться в своей группе через другого бота. Вы можете это сделать по кнопке ниже:', reply_markup=registration)
    
    print(query)
    
    



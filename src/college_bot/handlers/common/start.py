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
    become_leader = InlineKeyboardMarkup (
        inline_keyboard=[[
            InlineKeyboardButton(
                text="Стать старостой этой группы",
                callback_data='become_leader'
                )]
    ])

    if len(query) > 0:
        group = query[0]['group_id']
        await message.answer(f'Вы зарегистрированы в группе {group}.')
        
        headman = True # TODO: -> check headman in group
        
        if headman:
            await message.answer(f'Вы староста своей группы')
        else:
            headmen_count = 1 # TODO: -> check headman count in group
            if headmen_count < 2:
                await message.answer(
                    f'Вы не являетесь старостой, но в этой группе меньше 2-х старост, у Вас есть возможность зарегистрироваться, как староста.',
                    reply_markup=become_leader)
            else:
                await message.answer('В Вашей группе уже зарегистрированы старосты, вы не можете зарегистрироваться')
        

        

    else:
        await message.answer('Вы не зарегистрированы в какой-либо группе....')
        await message.answer('Для дальнейшего использования бота Вам необходимо зарегистрироваться в своей группе через другого бота. Вы можете это сделать по кнопке ниже:', reply_markup=registration)
    
    print(query)
    
    



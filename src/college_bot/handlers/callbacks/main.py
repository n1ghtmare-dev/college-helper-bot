from aiogram import Router, F
from aiogram.types import Message, CallbackQuery


router = Router()



@router.callback_query(F.data == 'become_leader')
async def add_headmen(callback: CallbackQuery):
    user_id = callback.from_user.id
    
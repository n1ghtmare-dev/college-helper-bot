from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_registration_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(
                    text='Зарегистрироваться',
                    url='https://t.me/Iubip_assistant_bot',
                )]
            ])

def get_leader_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup (
            inline_keyboard=[[
                InlineKeyboardButton(
                    text="Стать старостой этой группы",
                    callback_data='become_leader'
                    )]
            ])

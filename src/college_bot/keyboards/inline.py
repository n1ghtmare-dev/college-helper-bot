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

def get_report_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(
                text='📝 Составить отчет',
                callback_data='create_report',
            )
        ]]
    )

def get_confirmation_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✏️ Изменить", callback_data="edit_report"),
            InlineKeyboardButton(text="📤 Отправить", callback_data="submit_report")
        ]
    ])

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import StateFilter
from states import ReportStates
from aiogram.fsm.context import FSMContext
from datetime import datetime
from utils.report_utils import calculate_percentage
from keyboards.inline import get_confirmation_kb
from utils.json_handler.data_manager import JsonDataManager
from config import settings
from aiogram import Bot


router = Router()
json_manager = JsonDataManager(settings.DB_CONFIG)


@router.callback_query(F.data == 'create_report')
async def create_report(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_reply_markup(reply_markup=None)

    await state.set_state(ReportStates.waiting_room)
    await callback.message.answer("Введите номер аудитории:")

@router.message(StateFilter(ReportStates.waiting_room))
async def process_room(message: Message, state: FSMContext):
    await state.update_data(room=message.text)
    await state.set_state(ReportStates.waiting_teacher)
    await message.answer("Преподаватель присутствует? (Да/Нет)")

@router.message(StateFilter(ReportStates.waiting_teacher))
async def process_teacher(message: Message, state: FSMContext):
    if message.text.lower() not in ["да", "нет"]:
        return await message.answer("Пожалуйста, ответьте 'Да' или 'Нет'")
    
    await state.update_data(teacher_present=message.text.lower() == "да")
    await state.set_state(ReportStates.waiting_students)
    await message.answer("Сколько студентов присутствует на паре?")

@router.message(StateFilter(ReportStates.waiting_students))
async def process_students(message: Message, state: FSMContext):
    if not message.text.isdigit():
        return await message.answer("Пожалуйста, введите число")
    
    await state.update_data(students_count=int(message.text))
    await state.set_state(ReportStates.waiting_photo)
    await message.answer("Пришлите фото аудитории")

@router.message(StateFilter(ReportStates.waiting_photo), F.photo)
async def process_photo(message: Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    data = await state.get_data()
    
    report_text = (
        f"📅 {datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
        f"🚪 Аудитория: {data['room']}\n"
        f"👨‍🏫 Преподаватель: {'Присутствует' if data['teacher_present'] else 'Отсутствует'}\n"
        f"👥 Студентов: {data['students_count']}\n"
        f"📊 Процент присутствия: {calculate_percentage(data['students_count'])}%"
    )
    
    await state.update_data(
        photo_id=photo_id,
        report_text=report_text
    )
    
    await message.answer_photo(
        photo_id,
        caption=report_text,
        reply_markup=get_confirmation_kb()
    )
    await state.set_state(ReportStates.confirmation)

@router.callback_query(StateFilter(ReportStates.confirmation), F.data == "edit_report")
async def edit_report(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await state.set_state(ReportStates.waiting_room)
    await callback.message.answer("Введите номер аудитории:")

@router.callback_query(StateFilter(ReportStates.confirmation), F.data == "submit_report")
async def submit_report(callback: CallbackQuery, state: FSMContext, bot: Bot):
    data = await state.get_data()
    
    report_data = {
        "Дата": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user id": callback.from_user.id,
        "Имя": callback.from_user.full_name,
        "Кабинет": data['room'],
        "Присутствие преподавателя": 'Присутствует' if data['teacher_present'] else 'Отсутствует',
        "Количество студентов": data['students_count'],
    }

    report_text = (
        f"📅 {datetime.now().strftime('%d.%m.%Y %H:%M')}\n"
        f"🚪 Аудитория: {data['room']}\n"
        f"👨‍🏫 Преподаватель: {'Присутствует' if data['teacher_present'] else 'Отсутствует'}\n"
        f"👥 Студентов: {data['students_count']}\n"
        f"📊 Процент присутствия: {calculate_percentage(data['students_count'])}%"
    )

    await json_manager.save_report_and_photo(bot, data['photo_id'], report_data)

    await bot.send_photo(
            chat_id=settings.TELEGRAM_GROUP,
            photo=data['photo_id'],
            caption=report_text,
            parse_mode="Markdown"
        )

    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.answer("Отчёт успешно отправлен!", show_alert=True)
    await state.clear()

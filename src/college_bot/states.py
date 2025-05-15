from aiogram.fsm.state import StatesGroup, State


class ReportStates(StatesGroup):
    waiting_room = State()
    waiting_teacher = State()
    waiting_students = State()
    waiting_photo = State()
    confirmation = State()

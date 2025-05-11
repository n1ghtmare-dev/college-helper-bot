from aiogram import Bot, Dispatcher
from config import settings
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode


dp = Dispatcher()
bot = Bot(
    token=settings.BOT_TOKEN.get_secret_value(),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp.include_router("")

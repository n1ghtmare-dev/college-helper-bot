from aiogram import Bot, Dispatcher
from config import settings
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from handlers.common.start import router as start_router
import logging



logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

dp = Dispatcher()
bot = Bot(
    token=settings.BOT_TOKEN.get_secret_value(),
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)

dp.include_router(start_router)

import asyncio 
from core.dispatcher import dp, bot
from background.tasks import start
from background.scheduler import BackgroundScheduler


async def main() -> None:
    scheduler = BackgroundScheduler()
    await scheduler.start()
    try:
        await dp.start_polling(bot)
    finally:
        await scheduler.stop()

if __name__ == "__main__":
    asyncio.run(main())
    # start()

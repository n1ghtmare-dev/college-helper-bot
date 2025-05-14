import logging 
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .tasks import Tasks


logger = logging.getLogger(__name__)

class BackgroundScheduler:
    def __init__(self):
        self.scheduler = AsyncIOScheduler(timezone='UTC')
        self._create_job()

    def _create_job(self):
        self.scheduler.add_job(Tasks.json_update, 'cron', hour=1, minute=0)
        
    async def start(self):
        "Start background tasks"
        self.scheduler.start()
        logger.info("Background scheduler started")

    async def stop(self):
        self.scheduler.shutdown()
        logger.info("Background scheduler stopped")


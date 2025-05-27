from apscheduler.schedulers.asyncio import AsyncIOScheduler  # type: ignore
from loguru import logger


scheduler = AsyncIOScheduler(timezone='Europe/Moscow')


async def setup_scheduler() -> None:
    # scheduler.add_job(
    #     func=,
    #     kwargs={},
    #     trigger='cron',
    #     day=1
    # )
    scheduler.start()
    logger.info('Scheduler started')

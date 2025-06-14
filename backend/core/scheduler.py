from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from .services import PetfinderService

scheduler = AsyncIOScheduler()


def start_scheduler():
    scheduler.add_job(
        PetfinderService.run_sync,
        trigger=IntervalTrigger(hours=1),
        name="Fetch adoptable dogs from Petfinder",
        replace_existing=True,
    )
    scheduler.start()

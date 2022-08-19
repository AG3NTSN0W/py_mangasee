import asyncio
from datetime import datetime
from repository.mangas import Mangas
from utils.logger import logger
from repository.downloads import Download
from apscheduler.schedulers.asyncio import AsyncIOScheduler


def tick():
    logger.info('Tick! The time is: %s' % datetime.now())


class AppScheduler():

    def __init__(self) -> None:
        pass

    @staticmethod
    def start_scheduler():
        try:
            scheduler = AsyncIOScheduler()
            scheduler.add_job(tick, 'interval', seconds=3)
            scheduler.start()
            asyncio.get_event_loop().run_forever()
        except Exception as e:
            logger.error(e)

    def get_latest_chapters(self) -> list[Download]:


        GET_MANGAS()

        Mangas.get_mangas()



        pass


import asyncio
from datetime import datetime
from service.downloader import Downloader
from utils.logger import logger

from repository.mangas import Mangas
from repository.downloads import Download, Downloads
from repository.chapters import Mangachapters

from service.get_chapters import Chapter, get_chapters
from apscheduler.schedulers.asyncio import AsyncIOScheduler


def tick():
    logger.info('Tick! The time is: %s' % datetime.now())


def get_missing_chapters(id: int, rss_url: str) -> list[Download]:
    all_chapters = get_chapters(rss_url)
    chapters_in_system = Mangachapters().get_all_manga_chapters(id)
    to_map = list(
        filter(lambda c: not c.chapterTitle in chapters_in_system, all_chapters))
    return list(map(lambda c: Download(id, c.title, c.link, c.chapterTitle), to_map))


class AppScheduler():

    def __init__(self) -> None:
        pass

    def test(self):
        # self.queue_latest_chapters()
        self.dowload_chaters()
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

    def queue_latest_chapters(self) -> None:
        for manga in Mangas().get_mangas():
            Downloads().add_downloads(get_missing_chapters(manga.id, manga.rssUrl))

    def dowload_chaters(self):
        Downloader().init_app_pool(Downloads().to_download())
        pass

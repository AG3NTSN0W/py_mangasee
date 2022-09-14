
import os
import asyncio
from service.downloader import Downloader
from utils.logger import logger

from repository.mangas_DB import Manga, Mangas
from repository.downloads_DB import Download, Downloads
from repository.chapters_DB import MangaChapter, Mangachapters
from resource.manga import bp as mangas_bp
from resource.chapter import bp as chapters_bp
from resource.notification import bp as noti_bp


from service.get_chapters import Chapter, get_chapters
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from flask import Flask

def get_missing_chapters(manga: Manga) -> list[Download]:
    all_chapters = get_chapters(manga.rssUrl)
    all_chapter_len = len(all_chapters)
    missing_chapters = []
    logger.info(f"Available Manga count: [{all_chapter_len}], Curent Manga count [{manga.count}]")
    if (not manga.count == all_chapter_len):
        missing_count = all_chapter_len - manga.count
        break_on_count = 0
        chapters_in_system = Mangachapters().get_all_manga_chapters(manga.id)
        for c in all_chapters:
            if (not c.chapterTitle in chapters_in_system):
                missing_chapters.append(
                    Download(manga.id, c.title, c.link, c.chapterTitle))
                break_on_count += 1
            if (break_on_count == missing_count):
                break
        return missing_chapters
    # if (not manga.latestDate == all_chapters[0].pubDate):
    #     c = all_chapters[0];
    #     missing_chapters.append(
    #                 Download(manga.id, c.title, c.link, c.chapterTitle))
    #     return missing_chapters


class AppScheduler():

    def __init__(self) -> None:
        pass

    @staticmethod
    def start_scheduler():
        try:
            scheduler = AsyncIOScheduler()
            scheduler.add_job(AppScheduler.queue_latest_chapters, 'interval',
                              hours=1, max_instances=1)
            scheduler.add_job(AppScheduler.dowload_chapters, 'interval',
                              hours=3, max_instances=1)
            scheduler.add_job(AppScheduler.flask)                
            scheduler.start()
            asyncio.get_event_loop().run_forever()
        except Exception as e:
            logger.error(e)

    @staticmethod
    def queue_latest_chapters() -> None:
        for manga in Mangas().get_mangas():
            missing_chapters = get_missing_chapters(manga)
            if (missing_chapters):
                Downloads().add_downloads(missing_chapters)

    @staticmethod
    def dowload_chapters():
        Downloader().init_app_pool(Downloads().to_download())
        pass

    @staticmethod
    def index_files():
        mangaId = {}
        for (root, dirs, file) in os.walk("./downloads"):
            for name in file + dirs:
                title = root.replace("downloads", "").replace(
                    "/", "").replace(".", "")
                if (not title):
                    continue

                if (not title in mangaId):
                    manga = Mangas().get_manga_by_title(title)
                    mangaId[title] = manga.id

                chapterTitle = name.replace(".png", "").replace(".pdf", "")
                mangaChapter = MangaChapter(
                    chapterTitle=chapterTitle, downloadDate="", id=mangaId[title], totalImages=0, totalPages=0)
                try:
                    Mangachapters().add_chapter(mangaChapter)
                except:
                    logger.warn(
                        f"Unable to add chapter to db: [{chapterTitle}]")

    @staticmethod
    def flask():
        app = Flask(__name__)
        app.register_blueprint(mangas_bp)
        app.register_blueprint(chapters_bp)
        app.register_blueprint(noti_bp)
        app.run(host='0.0.0.0', port=80)

    pass

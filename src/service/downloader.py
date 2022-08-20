from multiprocessing.dummy import Pool
import os
import time
from datetime import datetime
from repository.downloads import Download, Downloads
from repository.chapters import MangaChapter, Mangachapters
from utils.logger import logger
from utils.duration import duration
from service.save_img import save_images
from service.get_chapters import get_chapters, get_chapter
from service.download_img import DownloadImg
from repository.retry_config import save_retry_config


class Downloader:
    def __init__(self, split=False, pool=2, format="pdf"):
        self.pool_size = pool
        self.split = split
        self.format = format

        self.image_count = 0
        self.save_to_path = f"/downloads"
        pass

    def dowload_all_chapters(self, goto_url):
        try:
            if (goto_url == None or not goto_url):
                raise Exception("RSS url was not provided")
            self.goto_url = goto_url
            start = time.time()
            logger.info(f"Let the dowloading commence")
            self.dowload_all_chapters_start()
            duration(start)
        except Exception as e:
            logger.error(e)
        pass

    def dowload_chapter(self, goto_url, chapter):
        try:
            self.chapters = get_chapter(goto_url, chapter)

            if self.hasChapters():
                self.init_cli_pool()
            else:
                logger.error(
                    f"Chapter: [{chapter}] Not found for {self.title}")
        except Exception as e:
            logger.error(e)
        pass

    def retry_chapters(self, chapters):
        self.chapters = chapters
        self.init_cli_pool()
    pass

    def dowload_all_chapters_start(self):
        self.chapters = get_chapters(self.goto_url)
        title = self.chapters[0].title
        self.init_cli_pool()
        self.validate_Chapters(title)
        pass

    def init_cli_pool(self):
        if(not self.hasChapters()):
            raise Exception("No chapters found")
        self.total_chapters = len(self.chapters)
        # self.chapters = self.chapters[:1]
        self.chapters = self.pool_handler(self.pool_worker)
        self.retry_pool(self.pool_worker, save_retry_config)

    def init_app_pool(self, chapters: list[Download]):
        self.chapters = chapters
        self.chapters = self.pool_handler(self.app_pool_worker)
        self.retry_pool(self.app_pool_worker, Downloads().add_downloads)

    def pool_worker(self, chapter):
        try:
            goto_url = chapter.link
            img_list = DownloadImg().get_image_list(goto_url)
            if (img_list == None or not img_list):
                return
            file_name = goto_url.split(
                "/")[-1].replace(".html", "").replace("-", " ")

            save_images(self.split)(
                img_list, f'{self.save_to_path}/{chapter.title}', file_name, self.format)
        except Exception as e:
            if (e.args and len(e.args) >= 2):
                logger.error(
                    f"[{e.args[1]}]: An exception occurred: {e.args[0]}, {chapter.chapterTitle}")
                return chapter
            logger.error(e)
            return chapter

    def app_pool_worker(self, chapter: Download):
        try:
            img_list = DownloadImg().get_image_list(chapter.link)
            if (img_list == None or not img_list):
                return
            chunk = save_images(not chapter.merge)(
                img_list, f'{self.save_to_path}/{chapter.title}', chapter.chapterTitle, chapter.fileType)
            date = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
            Mangachapters().add_chapter(MangaChapter(
                chapter.id, chapter.chapterTitle, date, len(img_list), chunk))
        except Exception as e:
            if (e.args and len(e.args) >= 2):
                logger.error(
                    f"[{e.args[1]}]: An exception occurred: {e.args[0]}, {chapter.chapterTitle}")
                return chapter
            logger.error(e)
            return chapter

    def pool_handler(self, worker):
        if(not self.hasChapters()):
            return
        with Pool(self.pool_size) as pool:
            return list(filter(lambda x: not x == None, pool.map(worker, self.chapters)))

    def retry_pool(self, worker, fallback):
        count = 0
        # Check if there are chapters that faild to download.
        if(self.hasChapters()):
            while count < 2:
                logger.error(
                    f"[{count}] Retrying missing Chapter Total: [{len(self.chapters)}]")
                self.chapters = self.pool_handler(worker)
                # Check if there are chapters that faild to download.
                if(not self.hasChapters()):
                    break
                count += 1
        if(self.hasChapters()):
            fallback(self.chapters)

    # validate that all chapter were downloaded
    def validate_Chapters(self, title):
        path = f"{self.save_to_path}/{title}"
        if(not os.path.exists(path)):
            logger.error(
                f"Unable to validate chaptes, Path does not exist: {path}")
            return
        if(len(os.listdir(path)) == self.total_chapters):
            logger.info(
                f"All {self.total_chapters} Chapter has been accounted for")
            return
        missingCount = self.total_chapters - len(os.listdir(path))
        logger.error(
            f"Hmm Looks like we are missing {missingCount} Chapters: Total: {self.total_chapters} ")

    def hasChapters(self):
        return (self.chapters and not self.chapters == None and len(self.chapters) > 0)

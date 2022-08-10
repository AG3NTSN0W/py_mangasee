from mimetypes import init
import requests
import datetime
from bs4 import BeautifulSoup

from utils.logger import logger


class Chapter():

    def __init__(self, title, chapterTitle, link, pubDate) -> None:
        self.title = title
        self.chapterTitle = chapterTitle
        self.link = link
        self.pubDate = pubDate
        pass

    def get_title(self):
        return self.title

    def get_chapterTitle(self):
        return self.chapterTitle

    def get_link(self):
        return self.link

    def get_pubDate(self):
        return self.pubDate


def chapter_map(entry, title: str) -> Chapter:
    return Chapter(title, entry.title.text, entry.link.text.replace("-page-1", ""), datetime.datetime.strptime(f"{entry.pubDate.text}", '%a, %d %b %Y %H:%M:%S %z').timestamp())


def get_items(url: str) -> list[Chapter]:
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'xml')
        title = soup.find('image').title.text
        entry_map = map(lambda i: chapter_map(i, title), soup.find_all('item'))
        return list(entry_map)
    except Exception as e:
        logger.error(f"Unable to get chapters: {e}")
        return None


def get_chapters(url: str) -> list[Chapter]:
    logger.info(f"Get all chapters from: {url}")
    try:
        return get_items(url)
    except Exception as e:
        logger.error(f"Unable to get chapters: {e}")
        return None


def get_chapter(url: str, chapter: str) -> list[Chapter]:
    logger.info(f"Get chapter {chapter} from: {url}")
    try:
        items = get_items(url)
        entries = list(
            filter(lambda x: x.chapterTitle.split()[-1] == chapter, items))
        return entries
    except Exception as e:
        logger.error(f"Unable to get chapters: {e}")
        return None

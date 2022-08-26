import requests
import datetime
from bs4 import BeautifulSoup
from repository.mangas import Manga

from utils.logger import logger


class Chapter():

    def __init__(self, title, chapterTitle, link, pubDate) -> None:
        self.title = title
        self.chapterTitle = chapterTitle
        self.link = link
        self.pubDate = pubDate
        pass

    def to_json(self) -> dict:
        return {
            "title": self.title,
            "chapterTitle": self.chapterTitle,
            "link": self.link,
            "pubDate": self.pubDate
        }


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

def get_manga_info(url: str, fileType: str = 'pdf', merge: bool = True) -> Manga:
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'xml')
        img = soup.find('image')
        title = img.title.text
        imgUrl = img.url.text
        latestDate = datetime.datetime.strptime(f"{soup.find_all('item')[0].pubDate.text}", '%a, %d %b %Y %H:%M:%S %z').timestamp()
        return Manga.constructor(title, url, latestDate, imgUrl, fileType, merge)
    except Exception as e:
        logger.error(f"Unable to get chapters: {e}")
        return None

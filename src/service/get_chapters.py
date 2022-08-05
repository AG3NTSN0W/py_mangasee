import logging
import requests
import datetime
from bs4 import BeautifulSoup

from utils.logger import logger 

def chapter_map(entry): 
  return {
    "title": entry.title.text,
    "link": entry.link.text.replace("-page-1",""),
    "pubDate": datetime.datetime.strptime(f"{entry.pubDate.text}", '%a, %d %b %Y %H:%M:%S %z').timestamp()
  }

def get_items(url):
    try: 
      page = requests.get(url)
      soup = BeautifulSoup(page.content, 'xml')
      title = soup.find('image').title.text
      return (title, list(map(chapter_map, soup.find_all('item'))))
    except Exception as e:
      logger.error(f"Unable to get chapters: {e}")
      return None


def get_chapters(url):
  logger.info(f"Get all chapters from: {url}")
  try: 
    title, items = get_items(url)
    entries = list(map(chapter_map, items))
    return (title, entries)
  except Exception as e:
    logger.error(f"Unable to get chapters: {e}")
    return None

def get_chapter(url, chapter):
  logger.info(f"Get chapter {chapter} from: {url}")
  try: 
    title, items = get_items(url)
    entries = list(filter(lambda x: x['title'].split()[-1] == chapter, items))
    return (title, entries)
  except Exception as e:
    logger.error(f"Unable to get chapters: {e}")
    return None    
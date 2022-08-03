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

def get_chapters(url):
  logger.info(f"Get all chapters from: {url}")
  try: 
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'xml')
    title = soup.find('image').title.text
    entries = list(map(chapter_map, soup.find_all('item')))
    return (title, entries)
  except Exception as e:
    logger.error(f"Unable to get chapters: {e}")
    return None
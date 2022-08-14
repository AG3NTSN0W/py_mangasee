
import sqlite3
from typing import List
from utils.logger import logger
from repository.database import Database


class Download:

    def __init__(self, title, chapterUrl, chapterTitle) -> None:
        self.title = title
        self.chapterUrl = chapterUrl
        self.chapterTitle = chapterTitle
        pass

    def to_tuple(self):
        return (self.title, self.chapterUrl, self.chapterTitle)


SELECT_TO_DOWNLOAD = """
SELECT TITLE, CHAPTER_URL, CHAPTER_TITLE FROM {table_name} LIMIT 100;
"""

DELETE_TO_DOWNLOAD = """
DELETE FROM {table_name} LIMIT 100;
"""

ADD_TO_DOWNLOAD = """
INSERT INTO {table_name}(TITLE, CHAPTER_URL, CHAPTER_TITLE) VALUES(?, ?, ?);
"""

GET_DOWNLOAD = """
SELECT TITLE, CHAPTER_URL, CHAPTER_TITLE FROM {table_name};
"""


class Downloads(Database):

    def __init__(self) -> None:
        super().__init__()

    def to_download(self) -> List[Download]:
        try:
            select_quary = SELECT_TO_DOWNLOAD.format(
                table_name=self.download_table_name)
            delete_quary = DELETE_TO_DOWNLOAD.format(
                table_name=self.download_table_name)
            with sqlite3.connect(f'{self.path}/{self.db_name}.db') as conn:
                cursor = conn.cursor()
                cursor.execute(select_quary)
                result = cursor.fetchall()
                cursor.execute(delete_quary)
                conn.commit()
            return list(map(lambda x: Download(*x), result))
        except Exception as e:
            logger.error("error", e)
        pass
        return

    def add_downlaod(self, download: Download):
        try:
            quary = ADD_TO_DOWNLOAD.format(table_name=self.download_table_name)
            with sqlite3.connect(f'{self.path}/{self.db_name}.db') as conn:
                cursor = conn.cursor()
                cursor.execute(quary, download.to_tuple())
                conn.commit()

            return cursor.rowcount
        except Exception as e:
            logger.error("error", e)
        pass

    def add_downlaods(self, downloads: List[Download]):
        try:
            quary = ADD_TO_DOWNLOAD.format(table_name=self.download_table_name)
            batch = list(map(lambda x: x.to_tuple(), downloads))
            with sqlite3.connect(f'{self.path}/{self.db_name}.db') as conn:
                cursor = conn.cursor()
                cursor.executemany(quary, batch)
                conn.commit()

            return cursor.rowcount
        except Exception as e:
            logger.error("error", e)
        pass

    def get_download(self) -> List[Download]:
        try:
            quary = GET_DOWNLOAD.format(table_name=self.download_table_name)
            with sqlite3.connect(f'{self.path}/{self.db_name}.db') as conn:
                cursor = conn.cursor()
                cursor.execute(quary)
                result = cursor.fetchall()
                conn.commit()

            return list(map(lambda x: Download(*x), result))
        except:
            logger.error("error")

from typing import List
from utils.logger import logger
from repository.database import Database


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


class Download:

    def __init__(self, title, chapterUrl, chapterTitle) -> None:
        self.title = title
        self.chapterUrl = chapterUrl
        self.chapterTitle = chapterTitle
        pass

    def to_tuple(self):
        return (self.title, self.chapterUrl, self.chapterTitle)


class Downloads(Database):

    def __init__(self) -> None:
        super().__init__()

    def to_download(self) -> List[Download]:
        select_query = self.query(SELECT_TO_DOWNLOAD, self.download_table_name)
        delete_query = self.query(DELETE_TO_DOWNLOAD, self.download_table_name)
        logger.info("Get Chapter to download")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(select_query)
            result = cursor.fetchall()
            cursor.execute(delete_query)
            conn.commit()
        return list(map(lambda x: Download(*x), result))

    def add_downlaod(self, download: Download):
        query = self.query(ADD_TO_DOWNLOAD, self.download_table_name)
        logger.info("Add Chapter to downloads")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, download.to_tuple())
            conn.commit()

        return cursor.rowcount

    def add_downlaods(self, downloads: List[Download]):
        query = self.query(ADD_TO_DOWNLOAD, self.download_table_name)
        batch = list(map(lambda x: x.to_tuple(), downloads))
        logger.info("Add batch of Chapter to download")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.executemany(query, batch)
            conn.commit()

        return cursor.rowcount

    def get_download(self) -> List[Download]:
        query = self.query(GET_DOWNLOAD, self.download_table_name)
        logger.info("Get all chapters")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            conn.commit()

        return list(map(lambda x: Download(*x), result))

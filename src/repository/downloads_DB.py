from utils.logger import logger
from repository.database import Database


SELECT_TO_DOWNLOAD = """
SELECT
    D.ID,
	D.TITLE,
	D.CHAPTER_URL,
	D.CHAPTER_TITLE,
	M.FILE_TYPE,
	M."MERGE",
    D.RETRY_COUNT
FROM
	{table_name} AS D
INNER join {M} AS M ON
	M.ID = D.ID	
WHERE D.RETRY_COUNT < 3      
ORDER BY D.CHAPTER_TITLE  
LIMIT 50;
"""

DELETE_TO_DOWNLOAD = """
DELETE
FROM
	{table_name} AS D
WHERE D.RETRY_COUNT < 3         
ORDER BY D.CHAPTER_TITLE  
LIMIT 50;
"""

ADD_TO_DOWNLOAD = """
INSERT INTO {table_name}(ID, TITLE, CHAPTER_URL, CHAPTER_TITLE, RETRY_COUNT) VALUES(?, ?, ?, ?, ?);
"""

GET_DOWNLOAD = """
SELECT ID, TITLE, CHAPTER_URL, CHAPTER_TITLE FROM {table_name};
"""
# 594


class Download:

    def __init__(self, id: int, title: str, link: str, chapterTitle: str, fileType: str = 'pdf', merge: int = 1, retryCount: int = 0) -> None:
        self.id = id
        self.title = title
        self.link = link
        self.chapterTitle = chapterTitle
        self.fileType = fileType
        self.merge = bool(merge)
        self.retryCount = retryCount
        pass

    def to_tuple(self):
        return (self.id, self.title, self.link, self.chapterTitle, self.retryCount)


class Downloads(Database):

    def __init__(self) -> None:
        super().__init__()

# TODO: Update Tests
    def to_download(self) -> list[Download]:
        select_query = SELECT_TO_DOWNLOAD.format(
            table_name=self.download_table_name, M=self.mangas_table_name)
        delete_query = self.query(DELETE_TO_DOWNLOAD, self.download_table_name)
        logger.info("Get Chapter to download")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(select_query)
            result = cursor.fetchall()
            cursor.execute(delete_query)
            conn.commit()
        return list(map(lambda x: Download(*x), result))

    def add_download(self, download: Download):
        query = self.query(ADD_TO_DOWNLOAD, self.download_table_name)
        logger.info("Add Chapter to downloads")
        with self.get_connection() as conn:
            conn.execute("PRAGMA foreign_keys = 1")
            cursor = conn.cursor()
            cursor.execute(query, download.to_tuple())
            conn.commit()

        return cursor.rowcount

    def add_downloads(self, downloads: list[Download]):
        query = self.query(ADD_TO_DOWNLOAD, self.download_table_name)
        batch = list(map(lambda d: d.to_tuple(), downloads))
        logger.info("Add batch of Chapter to download")
        with self.get_connection() as conn:
            conn.execute("PRAGMA foreign_keys = 1")
            cursor = conn.cursor()
            cursor.executemany(query, batch)
            conn.commit()

        return cursor.rowcount

    def get_download(self) -> list[Download]:
        query = self.query(GET_DOWNLOAD, self.download_table_name)
        logger.info("Get all chapters")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            conn.commit()

        return list(map(lambda x: Download(*x), result))

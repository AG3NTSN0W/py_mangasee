from utils.logger import logger
from repository.database import Database

# CHAPTER_TITLE   CHAR(255)               NOT NULL,
# DOWNLOAD_DATE   CHAR(50)                NOT NULL,
# TOTAL_IMAGES    INTEGER                 NOT NULL,
# TOTAL_PAGES     INTEGER     DEFAULT 0           ,
# ID              INTEGER                 NOT NULL,

ADD_CHAPTER = """
INSERT INTO {table_name}(ID, CHAPTER_TITLE, DOWNLOAD_DATE, TOTAL_IMAGES, TOTAL_PAGES) VALUES(?, ?, ?, ?, ?);
"""

GET_CHAPTERS = """
SELECT ID, CHAPTER_TITLE, DOWNLOAD_DATE, TOTAL_IMAGES, TOTAL_PAGES FROM {table_name} WHERE ID = ?
"""

DELETE_CHAPTERS = """
DELETE FROM {table_name} WHERE ID=?; 
"""

DELETE_CHAPTER = """
DELETE FROM {table_name} WHERE ID=? AND CHAPTER_TITLE=?; 
"""

UPDATE_CHAPTER = """
UPDATE {table_name} SET DOWNLOAD_DATE = ?, TOTAL_IMAGES = ?, TOTAL_PAGES = ? WHERE ID = ? AND CHAPTER_TITLE = ?;
"""

GET_ALL_CHAPTERS = """
select
	CHAPTER_TITLE
from
	{D}
WHERE ID = ?
union all
select
	CHAPTER_TITLE
from
	{C}
WHERE ID = ?	
"""


class MangaChapter():

    def __init__(self, id: int, chapterTitle: str, downloadDate: str, totalImages: int, totalPages: int) -> None:
        self.id = id
        self.chapterTitle = chapterTitle
        self.downloadDate = downloadDate
        self.totalImages = totalImages
        self.totalPages = totalPages
        pass

    def to_tuple(self) -> tuple:
        return (self.id, self.chapterTitle, self.downloadDate, self.totalImages, self.totalPages)

    def to_update(self) -> tuple:
        return (self.downloadDate, self.totalImages, self.totalPages)


class Mangachapters(Database):

    def __init__(self) -> None:
        super().__init__()

    def add_chapter(self, chapter: MangaChapter) -> bool:
        query = self.query(ADD_CHAPTER, self.chapters_table_name)
        logger.info("Add new Chapter")
        with self.get_connection() as conn:
            conn.execute("PRAGMA foreign_keys = 1")
            cursor = conn.cursor()
            cursor.execute(query, chapter.to_tuple())
            conn.commit()
        return cursor.rowcount == 1

    def get_manga_chapter(self, id: int) -> list[MangaChapter]:
        query = self.query(GET_CHAPTERS, self.chapters_table_name)
        logger.info("Get all manga chapters")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, [id])
            result = cursor.fetchall()

        return list(map(lambda x: MangaChapter(*x), result))

# TODO: Add tests
    def get_all_manga_chapters(self, id: int) -> list[str]:
        query = GET_ALL_CHAPTERS.format(
            D=self.download_table_name, C=self.chapters_table_name)
        logger.info("Get all chapters form downlaod and chapter table")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, [id, id])
            result = cursor.fetchall()
        return list(map(lambda r: r[0], result))

    def delete_manga_chapters(self, id: int) -> bool:
        query = self.query(DELETE_CHAPTERS, self.chapters_table_name)
        logger.info(f"Delete chapter by id: [{id}]")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, [id])
            conn.commit()

        return cursor.rowcount >= 1

    def delete_manga_chapter(self, id: int, chapterTitle: str) -> bool:
        query = self.query(DELETE_CHAPTER, self.chapters_table_name)
        logger.info(f"Delete chapter by id: [{id}]")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, [id, chapterTitle])
            conn.commit()

        return cursor.rowcount >= 1

    def update_manga_chapter(self, id: int, chapterTitle: str, chapter: MangaChapter) -> bool:
        query = self.query(UPDATE_CHAPTER, self.chapters_table_name)
        logger.info(f"Update manga ID: [{id}]")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (*chapter.to_update(), id, chapterTitle))
            conn.commit()

        return cursor.rowcount == 1

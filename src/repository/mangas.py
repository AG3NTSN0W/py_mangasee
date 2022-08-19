from utils.logger import logger
from repository.database import Database

# TITLE           CHAR(255)                  NOT NULL,
# RSS_URL         TEXT                       NOT NULL,
# CHAPTER_COUNT   INTEGER                    NOT NULL,
# LATEST_DATE     INTEGER                    NOT NULL,
# IMG_URL         TEXT                       NOT NULL,
# FILE_TYPE       CHAR(10)    DEFAULT "pdf"          ,
# MERGE           BOOLEAN     DEFAULT TRUE

ADD_MANGA = """
INSERT INTO {table_name}(TITLE, RSS_URL, LATEST_DATE, IMG_URL, FILE_TYPE, MERGE) VALUES(?, ?, ?, ?, ?, ?);
"""

# SELECT ID, TITLE, RSS_URL, LATEST_DATE, IMG_URL, FILE_TYPE, MERGE FROM {table_name} ;
GET_MANGAS = """
SELECT 
    M.ID,
    M.TITLE,
    M.RSS_URL,
    M.LATEST_DATE,
    M.IMG_URL,
    M.FILE_TYPE,
    M.MERGE,
    (D.CNT + C.CNT)
    MERGE FROM {table_name} AS M 
    LEFT JOIN
        (SELECT ID, COUNT(ID) AS CNT FROM {D}) AS D
        ON M.ID=D.ID
    LEFT JOIN
        (SELECT ID, COUNT(ID) AS CNT FROM {C}) AS C
        ON M.ID=C.ID    
    GROUP BY M.ID;
"""

GET_MANGAS_BY_ID = """
SELECT 
    M.ID,
    M.TITLE,
    M.RSS_URL,
    M.LATEST_DATE,
    M.IMG_URL,
    M.FILE_TYPE,
    M.MERGE,
    (D.CNT + C.CNT)
    MERGE FROM {table_name} AS M 
    LEFT JOIN
        (SELECT COUNT(ID) AS CNT FROM {D}) AS D
        ON M.ID=ID
    LEFT JOIN
        (SELECT COUNT(ID) AS CNT FROM {C}) AS C
        ON M.ID=ID    
    WHERE M.ID = ?    
    GROUP BY M.ID;
"""

GET_MANGAS_BY_TITLE = """
SELECT ID, TITLE, RSS_URL, LATEST_DATE, IMG_URL, FILE_TYPE, MERGE FROM {table_name} WHERE TITLE = ?;
"""

UPDATE_LAST_DATE = """
UPDATE {table_name} SET LATEST_DATE = ? WHERE ID = ?;
"""

UPDATE_MANGA = """
UPDATE {table_name} SET TITLE = ?, RSS_URL = ?, LATEST_DATE = ?, IMG_URL = ?, FILE_TYPE = ?, MERGE = ?  WHERE ID = ?;
"""

DELETE_MANGA_BY_ID = """
DELETE FROM {table_name} WHERE ID=?;
"""


class Manga():

    def __init__(self, id: int, title: str, rssUrl: str, latestDate: int, imgUrl: str, fileType: str, merge: bool, count=0) -> None:
        self.id = id
        self.title = title
        self.rssUrl = rssUrl
        self.latestDate = latestDate
        self.imgUrl = imgUrl
        self.fileType = fileType
        self.merge = bool(merge) 
        self.count = count
        pass

    @classmethod
    def constructor(cls, title: str, rssUrl: str, latestDate: int, imgUrl: str, fileType: str, merge: bool):
        return cls(None, title, rssUrl, latestDate, imgUrl, fileType, merge)

    def to_tuple(self) -> tuple:
        return (self.title, self.rssUrl, self.latestDate, self.imgUrl, self.fileType, self.merge)


class Mangas(Database):

    def __init__(self) -> None:
        super().__init__()

    def add_manga(self, manga: Manga) -> bool:
        query = self.query(ADD_MANGA, self.mangas_table_name)
        logger.info("Add new manga")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, manga.to_tuple())
            conn.commit()

        return cursor.lastrowid

    def get_mangas(self) -> list[Manga]:
        query = GET_MANGAS.format(
            table_name=self.mangas_table_name, D=self.download_table_name, C=self.chapters_table_name)
        logger.info("Get all mangas")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
        return list(map(lambda x: Manga(*x), result))

    def get_manga_by_title(self, title: str) -> Manga:
        query = self.query(GET_MANGAS_BY_TITLE, self.mangas_table_name)
        logger.info("Get mangas by title")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, [title])
            result = cursor.fetchone()
        return Manga(*result)

    def get_manga_by_id(self, id: int) -> Manga:
        query = GET_MANGAS_BY_ID.format(
            table_name=self.mangas_table_name, D=self.download_table_name, C=self.chapters_table_name)
        logger.info("Get mangas by id")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, [id])
            result = cursor.fetchone()

        return Manga(*result)

    def update_manga(self, manga: Manga, id: int) -> bool:
        query = self.query(UPDATE_MANGA, self.mangas_table_name)
        logger.info(f"Update manga ID: [{manga.id}]")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (*manga.to_tuple(), id))
            conn.commit()

        return cursor.rowcount == 1

    def update_manga_date(self, id: int, date: str) -> bool:
        query = self.query(UPDATE_LAST_DATE, self.mangas_table_name)
        logger.info(f"Update manga chapter count ID: [{id}], date: [{date}]")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (date, id))
            conn.commit()

        return cursor.rowcount == 1

    def delete_manga(self, id: int) -> bool:
        query = self.query(DELETE_MANGA_BY_ID, self.mangas_table_name)
        logger.info(f"Delete manga by id: [{id}]")
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, [id])
            conn.commit()

        return cursor.rowcount == 1

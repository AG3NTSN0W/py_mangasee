from repository.database import Database

class setupDataBase(Database):

    def __init__(self) -> None:
        super().__init__()

    def setup(self):
        self.create_manga_table()
        self.create_download_table()
        self.create_chapters_table()
        pass

    def create_manga_table(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self.mangas_table_name}
                (
                ID              INTEGER     PRIMARY KEY     NOT NULL,
                TITLE           CHAR(255)                   NOT NULL,
                RSS_URL         TEXT                        NOT NULL,
                LATEST_DATE     INTEGER                     NOT NULL,
                IMG_URL         TEXT                        NOT NULL,
                FILE_TYPE       CHAR(10)    DEFAULT "pdf"           ,
                MERGE           BOOLEAN     DEFAULT TRUE            ,
                UNIQUE(RSS_URL, TITLE)
                )''')
        pass

    def create_download_table(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self.download_table_name}
                (
                TITLE           CHAR(255)     NOT NULL,
                CHAPTER_URL     TEXT          NOT NULL,
                CHAPTER_TITLE   CHAR(255)     NOT NULL,
                ID              INTEGER       NOT NULL,
                RETRY_COUNT     INTEGER       DEFAULT 0, 
                FOREIGN KEY(ID) REFERENCES {self.mangas_table_name}(ID)
                UNIQUE(CHAPTER_TITLE)
                )''')
        pass

    def create_chapters_table(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f'''CREATE TABLE IF NOT EXISTS {self.chapters_table_name}
                (
                CHAPTER_TITLE   CHAR(255)               NOT NULL,
                DOWNLOAD_DATE   CHAR(50)                NOT NULL,         
                TOTAL_IMAGES    INTEGER                 NOT NULL,
                TOTAL_PAGES     INTEGER     DEFAULT 0           ,
                ID              INTEGER                 NOT NULL,
                FOREIGN KEY(ID) REFERENCES {self.mangas_table_name}(ID)
                UNIQUE(CHAPTER_TITLE)
                )''')
        pass

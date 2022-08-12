
from turtle import st


class Database():

    def __init__(self) -> None:
        self.path = "config/db"
        self.db_name = "mangaSee"
        
        self.download_table_name = 'download'
        self.mangas_table_name = 'mangas'
        self.chapters_table_name = 'chapters'
        pass

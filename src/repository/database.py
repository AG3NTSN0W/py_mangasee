import os
import sqlite3


class Database():

    def __init__(self) -> None:
        self.path = "config/db"
        self.db_name = "mangaSee"

        self.download_table_name = 'downloads'
        self.mangas_table_name = 'mangas'
        self.chapters_table_name = 'chapters'
        pass

    def set_path(self, path) -> None:
        self.path = path

    def get_connection(self) -> sqlite3.Connection:
        db_path = os.path.join(self.path, self.db_name)
        return sqlite3.connect('{db_path}.db'.format(db_path=db_path))

    def query(self, query, table) -> str:
        return query.format(
            table_name=table)

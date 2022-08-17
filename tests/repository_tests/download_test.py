import unittest

import os
from repository.setup import setupDataBase
from repository.mangas import Mangas, Manga
from repository.downloads import Downloads, Download

TEST_DATA = [Download(1,f"title_{x}", f"url_{x}",
                      f"chapterTitle_{x}") for x in range(5)]

MANGA_TEST_DATA = [
    Manga.constructor(
        f'title_{1}', f'url_{x}', x, f'imgUrl_{x}', 'pdf', True) for x in range(5)
]

class TestDownloadDB(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestDownloadDB, self).__init__(*args, **kwargs)
        pass

    def setUp(self):
        self.setup()
        self.addTestData()

    def tearDown(self):
        db_path = os.path.join(self.mangas.path, self.mangas.db_name)
        os.remove('{db_path}.db'.format(db_path=db_path))

    def setup(self) -> None:
        self.dataBase = setupDataBase()
        self.dataBase.set_path(".")
        self.dataBase.setup()

        self.download = Downloads()
        self.download.set_path(".")

        self.mangas = Mangas()
        self.mangas.set_path(".")


    def addTestData(self) -> None:
        for m in MANGA_TEST_DATA:
            self.mangas.add_manga(m)
        self.download.add_downloads(TEST_DATA)
        pass

    def test_add_download(self):
        download = Download(1, "title", "url", "chapterTitle")
        result = self.download.add_download(download)
        self.assertTrue(result == 1)
        self.assertTrue(len(self.download.get_download()) == 6)

    def test_get_downloads(self):
        result = self.download.get_download()
        self.assertEquals(
            (1, 'title_0', 'url_0', 'chapterTitle_0'), result[0].to_tuple())

    def test_to_download(self):
        to_download = self.download.to_download()
        self.assertTrue(len(to_download) == 5)
        result = self.download.get_download()
        self.assertTrue(len(result) == 0)

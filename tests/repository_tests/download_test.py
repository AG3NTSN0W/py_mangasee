import unittest

from repository.downloads import Downloads, Download
from repository.setup import setupDataBase

TEST_DATA = [Download(f"title_{x}", f"url_{x}",
                      f"chapterTitle_{x}") for x in range(5)]


class TestDownloadDB(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.setup(cls)
        cls.addTestData(cls)

    def __init__(self, *args, **kwargs):
        super(TestDownloadDB, self).__init__(*args, **kwargs)
        pass

    def setup(self) -> None:
        self.dataBase = setupDataBase()
        self.dataBase.set_path(".")
        self.dataBase.setup()

        self.download = Downloads()
        self.download.set_path(".")

    def addTestData(self) -> None:
        self.download.add_downloads(TEST_DATA)
        pass

    def test_add_download(self):
        download = Download("title", "url", "chapterTitle")
        result = self.download.add_download(download)
        self.assertTrue(result == 1)
        self.assertTrue(len(self.download.get_download()) == 6)

    def test_get_downloads(self):
        result = self.download.get_download()
        self.assertEquals(
            ('title_0', 'url_0', 'chapterTitle_0'), result[0].to_tuple())

    def test_to_download(self):
        to_download = self.download.to_download()
        self.assertTrue(len(to_download) == 6)
        result = self.download.get_download()
        self.assertTrue(len(result) == 0)

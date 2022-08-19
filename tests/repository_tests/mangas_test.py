import unittest

import os
from repository.setup import setupDataBase
from repository.mangas import Mangas, Manga
from repository.chapters import Mangachapters, MangaChapter
from repository.downloads import Downloads, Download

TEST_DATA = [
    Manga.constructor(
        f'title_{x}', f'url_{x}', x, f'imgUrl_{x}', 'pdf', True) for x in range(5)
]

DOWNLOAD_TEST_DATA = [Download(1,f"title_{x}", f"url_{x}",
                      f"chapterTitle_{x}") for x in range(5)]

MANGA_CHAPTER_TEST_DATA_ID_1 = [
    MangaChapter(1, f"CHAPTER-1_{x}", "0", 2, 0) for x in range(5)
]


class TestMangasDB(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestMangasDB, self).__init__(*args, **kwargs)
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

        self.mangachapters = Mangachapters()
        self.mangachapters.set_path(".")

        self.download = Downloads()
        self.download.set_path(".")

        self.mangas = Mangas()
        self.mangas.set_path(".")

    def addTestData(self) -> None:
        for m in TEST_DATA:
            self.mangas.add_manga(m)
        for c in MANGA_CHAPTER_TEST_DATA_ID_1:
            self.mangachapters.add_chapter(c)    
        self.download.add_downloads(DOWNLOAD_TEST_DATA)    
        pass

    def test_get_mangas(self):
        result = self.mangas.get_mangas()
        self.assertEquals(
            ('title_0', 'url_0', 0, 'imgUrl_0', 'pdf', True), result[0].to_tuple())
        self.assertTrue(len(result) == 5)
        self.assertTrue(result[0].count == 10)
        self.assertTrue(result[1].count == None)
        self.assertTrue(result[2].count == None)
      
    def test_get_mangas_by_title(self):
        result = self.mangas.get_manga_by_title("title_3")
        self.assertEquals(
            ('title_3', 'url_3', 3, 'imgUrl_3', 'pdf', True), result.to_tuple())
        self.assertTrue(result.count == 0)      

    def test_get_manga_by_id(self):
        result = self.mangas.get_manga_by_id(4)
        self.assertEquals(
            ('title_3', 'url_3', 3, 'imgUrl_3', 'pdf', True), result.to_tuple())
        self.assertTrue(result.count == 10)    
        pass

    def test_update_manga_date(self):
        result = self.mangas.update_manga_date(4, 7)
        self.assertTrue(result)
        getManga = self.mangas.get_manga_by_title("title_3")
        self.assertEquals(
            ('title_3', 'url_3', 7, 'imgUrl_3', 'pdf', True), getManga.to_tuple())

    def test_update_manga(self):
        manga = Manga.constructor(
            f'title_y', f'url_y', 7, f'imgUrl_y', 'pdf', True)
        self.mangas.update_manga(manga, 3)
        getManga = self.mangas.get_manga_by_title("title_y")
        self.assertEquals(
            (f'title_y', f'url_y', 7, f'imgUrl_y', 'pdf', True), getManga.to_tuple())

    def test_delete_manga(self):
        result = self.mangas.delete_manga(2)
        self.assertTrue(result)
        result = self.mangas.get_mangas()
        self.assertEquals(
            ('title_0', 'url_0', 0, 'imgUrl_0', 'pdf', True), result[0].to_tuple())
        self.assertTrue(len(result) == 4)
        pass
    pass

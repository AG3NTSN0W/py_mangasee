import unittest

import os
from repository.setup import setupDataBase
from repository.mangas_DB import Mangas, Manga
from repository.chapters_DB import MangaChapter, Mangachapters

MANGA_TEST_DATA = [
    Manga.constructor(
        f'title_{1}', f'url_{x}', x, f'imgUrl_{x}', 'pdf', True) for x in range(5)
]

MANGA_CHAPTER_TEST_DATA_ID_1 = [
    MangaChapter(1, f"CHAPTER-1_{x}", "0", 2, 0) for x in range(5)
]

MANGA_CHAPTER_TEST_DATA_ID_2 = [
    MangaChapter(2, f"CHAPTER-2_{x}", "0", 2, 0) for x in range(2)
]


class TestChapterDB(unittest.TestCase):

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)

    def setUp(self):
        self.setup()
        self.addTestData()

    def tearDown(self):
        db_path = os.path.join(self.mangas.path, self.mangas.db_name)
        os.remove('{db_path}.sqlite3'.format(db_path=db_path))

    def setup(self) -> None:
        self.dataBase = setupDataBase()
        self.dataBase.set_path(".")
        self.dataBase.setup()

        self.mangachapters = Mangachapters()
        self.mangachapters.set_path(".")

        self.mangas = Mangas()
        self.mangas.set_path(".")

    def addTestData(self) -> None:
        for m in MANGA_TEST_DATA:
            self.mangas.add_manga(m)
        for c in MANGA_CHAPTER_TEST_DATA_ID_1:
            self.mangachapters.add_chapter(c)
        for c in MANGA_CHAPTER_TEST_DATA_ID_2:
            self.mangachapters.add_chapter(c)
        pass

    def test_get_manga_chapter(self):
        result = self.mangachapters.get_manga_chapter(1)
        self.assertTrue(len(result) == 5)
        self.assertEquals((1, f"CHAPTER-1_0", "0", 2, 0), result[0].to_tuple())

    def test_delete_manga_chapters(self):
        result = self.mangachapters.delete_manga_chapters(2)
        self.assertTrue(result)
        result = self.mangachapters.get_manga_chapter(2)
        self.assertTrue(len(result) == 0)

    def test_delete_manga_chapter(self):
        result = self.mangachapters.delete_manga_chapter(2, "CHAPTER-2_1")
        self.assertTrue(result)
        result = self.mangachapters.get_manga_chapter(2)
        self.assertTrue(len(result) == 1)   
        self.assertEquals((2, f"CHAPTER-2_0", "0", 2, 0), result[0].to_tuple()) 

    def test_update_manga_chapter(self):
        c = MangaChapter(2,"CHAPTER-2_1", "123", 22, 3)
        result = self.mangachapters.update_manga_chapter(2, "CHAPTER-2_1", c)
        self.assertTrue(result)    
        result = self.mangachapters.get_manga_chapter(2)   
        self.assertTrue(len(result) == 2)   
        self.assertEquals((2,"CHAPTER-2_1", "123", 22, 3), result[1].to_tuple()) 
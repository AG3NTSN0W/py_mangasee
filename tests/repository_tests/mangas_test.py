import unittest

import os
from repository.setup import setupDataBase
from repository.mangas import Mangas, Manga

TEST_DATA = [
    Manga.constructor(
        f'title_{x}', f'url_{x}', x, x, f'imgUrl_{x}', 'pdf', True) for x in range(5)
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

        self.mangas = Mangas()
        self.mangas.set_path(".")

    def addTestData(self) -> None:
        for m in TEST_DATA:
            self.mangas.add_manga(m)
        pass

    def test_get_mangas(self):
        result = self.mangas.get_mangas()
        self.assertEquals(
            ('title_0', 'url_0', 0, 0, 'imgUrl_0', 'pdf', 1), result[0].to_tuple())
        self.assertTrue(len(result) == 5)

    def test_get_mangas_by_title(self):
        result = self.mangas.get_manga_by_title("title_3")
        self.assertEquals(
            ('title_3', 'url_3', 3, 3, 'imgUrl_3', 'pdf', 1), result.to_tuple())

    def test_get_manga_by_id(self):
        result = self.mangas.get_manga_by_id(4)
        self.assertEquals(
            ('title_3', 'url_3', 3, 3, 'imgUrl_3', 'pdf', 1), result.to_tuple())
        pass

    def test_update_manga_chapter_count(self):
        result = self.mangas.update_manga_chapter_count(4, 7, 20)
        self.assertTrue(result)
        getManga = self.mangas.get_manga_by_title("title_3")
        self.assertEquals(
            ('title_3', 'url_3', 7, 20, 'imgUrl_3', 'pdf', 1), getManga.to_tuple())

    def test_update_manga(self):
        manga = Manga.constructor(
            f'title_y', f'url_y', 7, 7, f'imgUrl_y', 'pdf', True)
        self.mangas.update_manga(manga, 3)
        getManga = self.mangas.get_manga_by_title("title_y")
        self.assertEquals(
            (f'title_y', f'url_y', 7, 7, f'imgUrl_y', 'pdf', True), getManga.to_tuple())

    def test_delete_manga(self):
        result = self.mangas.delete_manga(2)
        self.assertTrue(result)
        result = self.mangas.get_mangas()
        self.assertEquals(
            ('title_0', 'url_0', 0, 0, 'imgUrl_0', 'pdf', 1), result[0].to_tuple())
        self.assertTrue(len(result) == 4)
        pass
    pass

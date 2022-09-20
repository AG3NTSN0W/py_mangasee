import unittest

import os
from repository.setup import setupDataBase
from repository.mangas_DB import Mangas, Manga
from repository.chapters_DB import Mangachapters, MangaChapter
from repository.downloads_DB import Downloads, Download

MANGA_TEST_DATA = [
    Manga.constructor(
        'The Beginning After the End', 'https://mangasee123.com/rss/The-Beginning-After-The-End.xml', 1, "https://temp.compsci88.com/cover/The-Beginning-After-The-End.jpg", 'pdf', True),
    Manga.constructor(
        f'My Hero Academia', f'https://mangasee123.com/rss/Boku-No-Hero-Academia.xml', 1, "https://temp.compsci88.com/cover/Boku-No-Hero-Academia.jpg", 'pdf', True),
    Manga.constructor(
        f'My Dress-Up Darling', f'https://mangasee123.com/rss/Sono-Bisque-Doll-Wa-Koi-Wo-Suru.xml', 1, f'https://temp.compsci88.com/cover/Sono-Bisque-Doll-Wa-Koi-Wo-Suru.jpg', 'pdf', True)
]

MANGA_CHAPTER_TEST_DATA_ID_1 = [
    MangaChapter(1, f"The Beginning After the End Episode {x}", "1", 0, 0) for x in range(5)
]

MANGA_CHAPTER_TEST_DATA_ID_2 = [
    MangaChapter(2, f"My Hero Academia No. {x}", "1", 2, 0) for x in range(2)
]

MANGA_CHAPTER_TEST_DATA_ID_3 = [
    MangaChapter(3, f"My Dress-Up Darling Chapter {x}", "1", 2, 0) for x in range(2)
]

DOWNLOAD_TEST_DATA_1 = [Download(1, 'The Beginning After the End', f"https://mangasee123.com/read-online/The-Beginning-After-The-End-chapter-{x + 7}.html",
                                 f"The Beginning After the End Episode {x + 7}") for x in range(5)]

DOWNLOAD_TEST_DATA_2 = [Download(2, f'My Hero Academia', f"https://mangasee123.com/read-online/Boku-No-Hero-Academia-chapter-{x + 7}.html",
                                 f"My Hero Academia No. {x + 7}") for x in range(5)]

DOWNLOAD_TEST_DATA_3 = [Download(3, f'My Dress-Up Darling', f"https://mangasee123.com/read-online/Sono-Bisque-Doll-Wa-Koi-Wo-Suru-chapter-{x + 7}",
                                 f"My Dress-Up Darling Chapter {x + 7}") for x in range(5)]


class TestMangasDB(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestMangasDB, self).__init__(*args, **kwargs)
        pass

    def setUp(self):
        self.setup()
        self.add_test_data()

    def tearDown(self):
        db_path = os.path.join(self.mangas.path, self.mangas.db_name)
        os.remove('{db_path}.sqlite3'.format(db_path=db_path))

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

    def add_test_data(self):
        for m in MANGA_TEST_DATA:
            self.mangas.add_manga(m)
        for c in MANGA_CHAPTER_TEST_DATA_ID_1 + MANGA_CHAPTER_TEST_DATA_ID_2 + MANGA_CHAPTER_TEST_DATA_ID_3:
            self.mangachapters.add_chapter(c)
        self.download.add_downloads(
            DOWNLOAD_TEST_DATA_1 + DOWNLOAD_TEST_DATA_2 + DOWNLOAD_TEST_DATA_3)
        pass

    def test_get_mangas(self):
        result = self.mangas.get_mangas()
        self.assertEquals(
            MANGA_TEST_DATA[0].to_tuple(), result[0].to_tuple())
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0].count, 10)
        self.assertEqual(result[1].count, 7)
        self.assertEqual(result[2].count, 7)

    def test_get_mangas_by_title(self):
        result = self.mangas.get_manga_by_title(MANGA_TEST_DATA[2].title)
        self.assertEquals(
            MANGA_TEST_DATA[2].to_tuple(), result.to_tuple())
        self.assertEqual(result.count, 0)

    def test_get_manga_by_id(self):
        result = self.mangas.get_manga_by_id(3)
        self.assertEquals(
            MANGA_TEST_DATA[2].to_tuple(), result.to_tuple())
        self.assertEqual(result.count, 7)
        pass

    def test_update_manga_date(self):
        result = self.mangas.update_manga_date(3, 7)
        self.assertTrue(result)
        getManga = self.mangas.get_manga_by_id(3)
        newValue = MANGA_TEST_DATA[2]
        newValue.latestDate = 7
        self.assertEquals(
            newValue.to_tuple(), getManga.to_tuple())

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
        self.assertEqual(len(result), 2)
        pass
    pass

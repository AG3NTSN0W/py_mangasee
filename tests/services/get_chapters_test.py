import unittest
from unittest import mock
from service.get_chapters import get_chapters, get_chapter, Chapter


class TestGetChapters(unittest.TestCase):

    MOCK_RSS = [
        Chapter(
            'The Beginning After the End',
            'The Beginning After the End Episode 154',
            'https://mangasee123.com/read-online/The-Beginning-After-The-End-chapter-154.html',
            1657933184.0
        ),
        Chapter(
            'The Beginning After the End',
            'The Beginning After the End Episode 153',
            'https://mangasee123.com/read-online/The-Beginning-After-The-End-chapter-153.html',
            1657307074.0
        ),
        Chapter(
            'The Beginning After the End',
            'The Beginning After the End Episode 152',
            'https://mangasee123.com/read-online/The-Beginning-After-The-End-chapter-152.html',
            1656701960.0
        )
    ]

    @mock.patch('service.get_chapters.get_items')
    def test_get_chapters_test(self, get_items):
        get_items.return_value = self.MOCK_RSS
        chapter_list = get_chapters("Test")
        self.assertEquals(self.MOCK_RSS, chapter_list)

    @mock.patch('service.get_chapters.get_items')
    def test_get_chapter_non_found_test(self, get_items):
        get_items.return_value = self.MOCK_RSS
        chapter_list = get_chapter("Test", "1")
        self.assertEquals([], chapter_list)

    @mock.patch('service.get_chapters.get_items')
    def test_get_chapter_test(self, get_items):
        get_items.return_value = self.MOCK_RSS
        chapter_list = get_chapter("Test", "152")
        self.assertEquals(
            'The Beginning After the End Episode 152', chapter_list[0].chapterTitle)
        self.assertEquals(
            'https://mangasee123.com/read-online/The-Beginning-After-The-End-chapter-152.html', chapter_list[0].link)

import os
import unittest
from service.download_img import DownloadImg, DownloadException

HTML_FILE = f'file:///{os.getcwd()}/tests/resources/test_page.html'


class TestDownloadImg(unittest.TestCase):

    max_width = 200
    current_width = 200
    current_height = 300
    percentage = 100.0
    downloadImg = DownloadImg()

    def test_get_img_list(self):
        img_list = self.downloadImg.get_image_list(HTML_FILE)
        self.assertTrue(len(img_list) == 1)
        self.assertEquals(
            list(img_list)[0].shape, (self.current_height, self.current_width, 3))

    def test_get_img_width(self):
        width = self.downloadImg.get_img_width(self.max_width)
        self.assertEquals(width, self.max_width)

    def test_get_percentage(self):
        percentage = self.downloadImg.get_percentage(
            self.max_width, self.current_width)
        self.assertEquals(percentage, self.percentage)

    def test_new_height(self):
        height = self.downloadImg.new_height(
            self.current_height, self.percentage)
        self.assertEquals(height, self.current_height)

    def test_get_dim(self):
        dim = self.downloadImg.get_dim(self.current_width, self.current_height)
        self.assertEquals(dim, (self.current_width, self.current_height))

    def test_get_img_list_error(self):
        with self.assertRaises(DownloadException):
            self.downloadImg.get_image_list("http://HTML_FILE")

    def test_get_percentage_invalid_max_width(self):
        with self.assertRaises(Exception):
            self.downloadImg.get_percentage(
                "200", self.current_width)

    def test_get_percentage_invalid_current_width(self):
        with self.assertRaises(Exception):
            self.downloadImg.get_percentage(
                self.max_width, "200")

    # TODO: Complete errors
    def test_new_height_error(self):
        height = self.downloadImg.new_height(
            self.current_height, self.percentage)
        self.assertEquals(height, self.current_height)

    def test_get_dim_error(self):
        dim = self.downloadImg.get_dim(self.current_width, self.current_height)
        self.assertEquals(dim, (self.current_width, self.current_height))

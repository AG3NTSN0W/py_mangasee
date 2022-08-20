import os
import cv2
import shutil
import unittest
from os.path import exists
from service.save_img import merge_all, save_images, to_file, save_type, to_png, to_pdf

IMG_PATH = f'{os.getcwd()}/tests/resources/237-200x300.jpg'
SAVE_PATH = "/downloads"


class TestSaveImg(unittest.TestCase):

    img_list = []

    def __init__(self, *args, **kwargs):
        super(TestSaveImg, self).__init__(*args, **kwargs)
        self.img_list.append(cv2.imread(IMG_PATH))
        pass

    def tearDown(self):
        for path in os.listdir(SAVE_PATH):
            nPath = os.path.join(SAVE_PATH, path)
            if os.path.isfile(nPath):
                os.remove(nPath)
                continue
            if (os.path.isdir(nPath)):
                shutil.rmtree(nPath)
                continue

    # SPLIT
    def test_save_images_png_split(self):
        save_images(True)(self.img_list,
                          f'{SAVE_PATH}', "ave_images_png_split", "png")
        self.assertTrue(
            exists(f"{SAVE_PATH}/ave_images_png_split/ave_images_png_split-000.png"))
    

    def test_save_images_pdf_split(self):
        chunk = save_images(True)(self.img_list,
                          f'{SAVE_PATH}', "save_images_pdf_split", "pdf")
        self.assertEqual(chunk, 1)                   
        self.assertTrue(
            exists(f"{SAVE_PATH}/save_images_pdf_split/save_images_pdf_split-000.pdf"))

    def test_to_file_png(self):
        to_file(self.img_list, f'{SAVE_PATH}', "to_file_png", "png")

        self.assertTrue(exists(f"{SAVE_PATH}/to_file_png/to_file_png-000.png"))

    def test_to_file_pdf(self):
        chunk = to_file(self.img_list, f'{SAVE_PATH}', "to_file_pdf")
        self.assertEqual(chunk, 1) 
        self.assertTrue(exists(f"{SAVE_PATH}/to_file_pdf/to_file_pdf-000.pdf"))

    # MERGE
    def test_save_images_png_merge(self):
        save_images()(self.img_list, f'{SAVE_PATH}',
                      "save_images_png_merge", "png")
        self.assertTrue(exists(f"{SAVE_PATH}/save_images_png_merge.png"))

    def test_save_images_pdf_merge(self):
        save_images()(self.img_list, f'{SAVE_PATH}', "save_images_pdf_merge")
        self.assertTrue(exists(f"{SAVE_PATH}/save_images_pdf_merge.pdf"))

    def test_merge_all_png(self):
        merge_all(self.img_list, f'{SAVE_PATH}', "png_merge_all", "png")
        self.assertTrue(exists(f"{SAVE_PATH}/png_merge_all.png"))

    def test_merge_all_pdf(self):
        chunk = merge_all(self.img_list, f'{SAVE_PATH}', "pdf_merge_all")
        self.assertEqual(chunk, 1)    
        self.assertTrue(exists(f"{SAVE_PATH}/pdf_merge_all.pdf"))

    # SAVE
    def test_save_type_png(self):
        img_list = cv2.vconcat(self.img_list)
        save_type()(img_list,  f"{SAVE_PATH}/save_type_png")
        self.assertTrue(exists(f"{SAVE_PATH}/save_type_png.png"))
        pass

    def test_save_type_pdf(self):
        img_list = cv2.vconcat(self.img_list)
        save_type('pdf')(img_list, f"{SAVE_PATH}/save_type_pdf")
        self.assertTrue(exists(f"{SAVE_PATH}/save_type_pdf.pdf"))
        pass

    def test_to_png(self):
        img_list = cv2.vconcat(self.img_list)
        to_png(img_list,  f"{SAVE_PATH}/to_png")
        self.assertTrue(exists(f"{SAVE_PATH}/to_png.png"))

    def test_to_pdf(self):
        img_list = cv2.vconcat(self.img_list)
        chunk = to_pdf(img_list, f"{SAVE_PATH}/to_pdf")
        self.assertEqual(chunk, 1)    
        self.assertTrue(exists(f"{SAVE_PATH}/to_pdf.pdf"))

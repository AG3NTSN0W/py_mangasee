import cv2
import time
import requests
import numpy as np
from utils.logger import logger
from utils.duration import duration
from service.web_scraper import get_manga_images, WebScraperException

# Mat = np.ndarray[int, np.dtype[np.generic]]


class DownloadImg():

    def __init__(self) -> None:
        self.img_width: int = 0
        pass

    def get_img_width(self, width: int) -> int:
        if self.img_width == 0:
            self.img_width = width
        return self.img_width

    def get_percentage(self, max_width: int, current_width: int) -> float:
        return (max_width / current_width) * 100

    def new_height(self, current_height: int, percentage: float) -> int:
        return round(current_height * (percentage/100))

    def get_dim(self, width: int, height: int) -> tuple[int, int]:
        max_width = self.get_img_width(width)
        percentage = self.get_percentage(max_width, width)
        new_height_percentage = self.new_height(height, percentage)
        logger.debug(
            f"Image dimensions - Width: [{max_width}], height: [{new_height_percentage}], percentage: [{percentage}]%")
        return (max_width, new_height_percentage)

    def downloaded_img(self, url_list: list[str]) -> list[cv2.Mat]:
        img_list = []
        for image_url in url_list:
            resp = requests.get(image_url, stream=True)
            if resp.status_code == 200:
                resp.raw.decode_content = True
                image = np.asarray(bytearray(resp.raw.read()), dtype="uint8")
                image = cv2.imdecode(image, cv2.IMREAD_COLOR)
                image = cv2.resize(image, self.get_dim(
                    image.shape[1], image.shape[0]))
                img_list.append(image)
            else:
                raise Exception(f'Unable to download {image_url}')
        return img_list

    def get_image_list(self, goto_url: str) -> list[cv2.Mat]:
        try:
            start = time.time()
            image_list = get_manga_images(goto_url)
            logger.info(
                f"Downoading {len(image_list)} images from URL [{goto_url}]")
            img_list = self.downloaded_img(image_list)
            if (not len(image_list) == len(img_list)):
                raise Exception('Failed to download all images')
            logger.info(
                f"All {len(image_list)} images from [{goto_url}] has been accounted for: Duration: [{duration(start)}]")
            return img_list
        except WebScraperException as e:
            raise DownloadException(e.args[1], e.args[0])
        except Exception as e:
            raise DownloadException(e, "download_img")


class DownloadException(Exception):
    def __init__(self, message, service):
        super(Exception, self).__init__(message, service)

# # Solo test
# def downloaded_and_save(goto_url, should_merge=True):
#     try:
#         image_list = get_manga_images(goto_url)
#         img_list = downloaded_img(image_list)
#         file_name = goto_url.split("/")[-1].replace(".html", "").replace("-", " ")
#         save_images(should_merge)(img_list, "./", file_name)
#     except Exception as e:
#         logger.error(f"An exception occurred: {e}")

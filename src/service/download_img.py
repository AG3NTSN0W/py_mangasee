import cv2
import asyncio
import logging
import requests
import numpy as np

from bs4 import BeautifulSoup

from service.save_img import save_images
from service.web_scraper import get_manga_images, WebScraperException

img_width = 0

from utils.logger import logger 

def get_img_width(width):
    global img_width
    if img_width == 0:
        img_width = width
    return img_width

def get_percentage(max_width, current_width):
    return (max_width / current_width) * 100

def new_hight(current_hight, percentage):
    return round(current_hight * (percentage/100))

def get_dim(width, hight):
    max_width = get_img_width(width)
    percentage = get_percentage(max_width, width)
    new_hight_percentage = new_hight(hight, percentage)
    logger.debug(f"Image dimensions - Width: [{max_width}], hight: [{new_hight_percentage}], percentage: [{percentage}]%")
    return (max_width, new_hight_percentage)    

def downloaded_img(url_list):
    img_list = []
    for image_url in url_list:
        resp = requests.get(image_url, stream = True)
        if resp.status_code == 200:
            resp.raw.decode_content = True
            image = np.asarray(bytearray(resp.raw.read()), dtype="uint8")
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)  
            image = cv2.resize(image, get_dim(image.shape[1], image.shape[0]))
            img_list.append(image)
        else:
            raise Exception(f'Unable to downlaod {image_url}')
    return img_list
    
def get_image_list(goto_url, should_merge=True):
    try:
        image_list = get_manga_images(goto_url)
        logger.info(f"Stated to Downloading {len(image_list)} images from: [{goto_url}]")
        img_list = downloaded_img(image_list)
        if (not len(image_list) == len(img_list)):
            raise Exception('Failed to download all images')
        logger.info(f"images from [{goto_url}] has been accounted for")  
        return img_list
    except WebScraperException as e:
        logger.info(f"{e}")  
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

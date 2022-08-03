import os
import cv2
import logging

from utils.logger import logger 

def merge_all(img_list, path, file_name):
    logger.info(f"[{file_name}]: All Image dowloaded starting with merge ...")
    
    try:
        os.makedirs(f"{path}", exist_ok=True)
        im_v = cv2.vconcat(img_list)
        img_name = os.path.join(path, file_name + ".png")
        cv2.imwrite(f'{img_name}', im_v)
        logger.info(f'Chapter saved: {file_name}.png',)
    except Exception as e:
        logger.error(f"An exception occurred: {e}")  
    pass

def to_file(img_list, path, file_name):
    try:
        path_name = os.path.join(path, file_name)
        os.makedirs(f"{path_name}", exist_ok=True)
        for (idx, img) in enumerate(img_list):
            indexFormat = '{:03}'.format(idx)
            img_name = os.path.join(path_name, f"{file_name}-{indexFormat}.png")
            logger.info(f"Saving the image to a file: {img_name}")
            cv2.imwrite(f"{img_name}", img)
    except Exception as e:
        logger.error(f"An exception occurred: {e}")  
    pass

def save_images(merge=True):
    if (merge):
        return merge_all
    return to_file   
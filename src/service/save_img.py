import os
import cv2
import logging
import img2pdf

from PIL import Image
from utils.logger import logger 

def to_png(im_v, img_name): 
    try:
        cv2.imwrite(f'{img_name}.png', im_v)
    except Exception as e:
        logger.error(f"An exception occurred: {e}")  
    pass

def to_pdf(im_v, img_name):
    try:
        im_pil = Image.fromarray(im_v)
        im_pil.save(f'{img_name}.pdf')
    except Exception as e:
        logger.error(f"An exception occurred: {e}")  
    pass

def save_type(type='png'):
    if (type.upper() == 'PNG'):
        return to_png    
    return to_pdf   

def to_file(img_list, path, file_name, type="pdf"):
    try:
        path_name = os.path.join(path, file_name)
        os.makedirs(f"{path_name}", exist_ok=True)
        for (idx, img) in enumerate(img_list):
            indexFormat = '{:03}'.format(idx)
            img_name = os.path.join(path_name, f"{file_name}-{indexFormat}")
            logger.debug(f"Saving the image to a file: {img_name}.{type}")
            save_type(type)(img, img_name)
    except Exception as e:
        logger.error(f"An exception occurred: {e}")  
    pass    

def merge_all(img_list, path, file_name, type="pdf"):
    logger.info(f"[{file_name}]: All Image dowloaded starting with merge ...")
    try:
        os.makedirs(f"{path}", exist_ok=True)
        im_v = cv2.vconcat(img_list)
        img_name = os.path.join(path, file_name)
        save_type(type)(im_v, img_name)
        logger.info(f'Chapter saved: {file_name}.{type}')
    except Exception as e:
        logger.error(f"An exception occurred: {e}")  
    pass

def save_images(split=False):
    if (split):
        return to_file   
    return merge_all
    
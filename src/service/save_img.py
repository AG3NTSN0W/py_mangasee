import os
import cv2
import math
import numpy as np

from PIL import Image
from utils.logger import logger 

def to_png(im_v, img_name: str) -> None: 
    cv2.imwrite(f'{img_name}.png', im_v)

def to_pdf(im_v, img_name: str) -> None:
    try:
        im_v = cv2.cvtColor(im_v, cv2.COLOR_RGB2BGR)
        # chunk = math.ceil((im_v.shape[0]/65500)) # max amount of pixels
        chunk = math.ceil((im_v.shape[0]/20000))
        if chunk >= 2:
            chunks = np.array_split(im_v, chunk)
            c = list(map(lambda x: Image.fromarray(x), chunks))
            c[0].save(f'{img_name}.pdf', save_all=True, append_images=c[1:])
            return (chunk)
        else:
            im_pil = Image.fromarray(im_v)
            im_pil.save(f'{img_name}.pdf') 
            return (chunk)              
    except Exception as e:
        logger.error(f"An exception occurred: {e}: Saving to png instead")  
        to_png(im_v, img_name)

def save_type(type='png'):
    if (type.upper() == 'PNG'):
        return to_png    
    return to_pdf   

def to_file(img_list, path: str, file_name: str, type="pdf") -> None:
    path_name = os.path.join(path, file_name)
    os.makedirs(f"{path_name}", exist_ok=True)
    for (idx, img) in enumerate(img_list):
        indexFormat = '{:03}'.format(idx)
        img_name = os.path.join(path_name, f"{file_name}-{indexFormat}")
        logger.debug(f"Saving the image to a file: {img_name}.{type}")
        return save_type(type)(img, img_name)
 

def merge_all(img_list: list[cv2.Mat], path: str, file_name: str, type="pdf") -> None:
    logger.info(f"[{file_name}]: All Image dowloaded starting with merge ...")
    os.makedirs(f"{path}", exist_ok=True)
    img_name = os.path.join(path, file_name)
    chunk = save_type(type)(cv2.vconcat(img_list), img_name)
    logger.info(f'Chapter saved: {file_name}.{type}')
    return chunk


def save_images(split=False):
    if (split):
        return to_file   
    return merge_all
    
import os
import cv2

from PIL import Image
from utils.logger import logger 

def to_img_arr(img):
    return Image.fromarray(img)

def to_png(img, img_name: str) -> None: 
    cv2.imwrite(f'{img_name}.png', img)

def to_pdf(img_list, img_name: str) -> None:
    try:
        # cv2.cvtColor(img_list, cv2.COLOR_RGB2BGR)
        img_arr = list(map(to_img_arr, img_list))
        img_arr[0].save(f'{img_name}.pdf', save_all=True, append_images=img_arr[1:])
    except Exception as e:
        logger.error(f"An exception occurred: {e}: Saving to png instead")
        to_png(cv2.vconcat(img_list), img_name)

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
        save_type(type)(img, img_name)
 

def merge_all(img_list: list[cv2.Mat], path: str, file_name: str, type="pdf") -> None:
    logger.info(f"[{file_name}]: All Image dowloaded starting with merge ...")
    os.makedirs(f"{path}", exist_ok=True)
    img_name = os.path.join(path, file_name)
    if(type.upper() == 'PNG'):
        img_list = cv2.vconcat(img_list)
    save_type(type)(img_list, img_name)
    logger.info(f'Chapter saved: {file_name}.{type}')


def save_images(split=False):
    if (split):
        return to_file   
    return merge_all
    
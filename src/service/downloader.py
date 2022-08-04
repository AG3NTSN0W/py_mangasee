import os
import time
from utils.logger import logger 
from utils.duration import duration 
from multiprocessing import Pool
from service.save_img import save_images
from service.get_chapters import get_chapters
from service.download_img import get_image_list
from repository.retry_config import save_retry_config

class Downloader:
    def __init__(self, split=False, pool=2, format="png"):
        self.pool_size = pool
        self.image_count = 0
        self.split = split
        self.format = format
        pass

    def dowload_all_chapters(self, goto_url):
        try:
            if (goto_url == None or not goto_url):
                raise Exception("RSS url was not provided")  
            self.goto_url = goto_url
            start = time.time()
            logger.info(f"Let the dowloading commence")
            self.dowload_all_chapters_start()
            duration(start)
        except Exception as e:
            logger.error(e)        
        pass

    def dowload_one_chapters(self, title, goto_url):
        try:
            self.save_to_path = f"/downloads/{self.title}"
            img_list = get_image_list(goto_url)
            if (img_list == None or not img_list):
                return
            file_name = goto_url.split("/")[-1].replace(".html", "").replace("-", " ")
            save_images(self.split)(img_list, self.save_to_path, file_name, self.format)
        except Exception as e:
            logger.error(e)        
        pass    

    def retry_chapters(self, title, chapters):
        self.title = title
        self.chapters = chapters
        self.init_pool()
    pass           

    def dowload_all_chapters_start(self):
        self.title, self.chapters = get_chapters(self.goto_url)
        self.init_pool()
        self.validate_Chapters() 
        pass  

    def init_pool(self):
        if(not self.hasChapters()):
            raise Exception("No chapters found")  
        self.total_chapters = len(self.chapters) 
        self.save_to_path = f"/downloads/{self.title}"
        # self.chapters = self.chapters[:1]
        self.chapters = self.pool_handler()
        self.retry_pool()
             
    def pool_worker(self, chapter):
            try:
                goto_url = chapter['link']
                img_list = get_image_list(goto_url)
                if (img_list == None or not img_list):
                    return
                file_name = goto_url.split("/")[-1].replace(".html", "").replace("-", " ")
                save_images(self.split)(img_list, self.save_to_path, file_name, self.format)
            except Exception as e:
                if (e.args and len(e.args) >= 2):
                    logger.error(f"[{e.args[1]}]: An exception occurred: {e.args[0]}, {chapter['title']}")
                    return chapter
                logger.error(e)
                return chapter

    def pool_handler(self):
        if(not self.hasChapters()):
            return
        with Pool(self.pool_size) as pool:
            return list(filter(lambda x: not x == None, pool.map(self.pool_worker, self.chapters)))

    def retry_pool(self):
        count = 0
        # Check if there are chapters that faild to download.
        if(self.hasChapters()):
            while count < 2:
                logger.error(f"Retrying missing Chapter: [{count}]")
                self.chapters = self.pool_handler()
                # Check if there are chapters that faild to download.
                if(not self.hasChapters()):
                    break
                count += 1  
        if(self.hasChapters()):
            save_retry_config(self.title, self.chapters)
            return              

    # validate that all chapter were downloaded
    def validate_Chapters(self):
        if(not os.path.exists(self.save_to_path)):
            logger.error(f"Unable to validate chaptes, Path does not exist: {self.save_to_path}")
            return
        if(len(os.listdir(self.save_to_path)) == self.total_chapters):
            logger.info(f"All {self.total_chapters} Chapter has been accounted for")
            return
        missingCount = self.total_chapters - len(os.listdir(self.save_to_path))    
        logger.error(f"Hmm Looks like we are missing {missingCount} Chapters: Total: {self.total_chapters} ")   

    def hasChapters(self):
        return (self.chapters and not self.chapters == None and len(self.chapters) > 0)
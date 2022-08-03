import os
from service.downloader import Downloader
from repository.retry_config import get_retry_config, save_retry_config, get_retry_path

def retry_from_config():
    for filename in os.scandir(get_retry_path()):
        if filename.is_file():
            file_name = filename.name.replace(".json", "")
            title, chapters = get_retry_config(file_name)
            Downloader().retry_chapters(title, chapters)

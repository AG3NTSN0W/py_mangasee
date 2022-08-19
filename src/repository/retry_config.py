import os
import json
import logging
from datetime import datetime

from service.get_chapters import Chapter


def get_retry_path():
    return "/config/retry"


def get_retry_config(file_name) -> list[dict]:
    try:
        logging.debug(f"Getting {file_name} retry config")
        json_file = open(f"{get_retry_path()}/{file_name}.json", "r")
        retry_json = json.load(json_file)
        json_file.close()
        logging.debug(f"Deleting {file_name} retry config")
        os.remove(f"{get_retry_path()}/{file_name}.json")
        return retry_json
    except:
        return []


def save_retry_config(chapters: list[Chapter]) -> None:
    try:
        title = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        if(not os.path.exists(get_retry_path())):
            logging.debug(f"Add missing retry config dir")
            os.makedirs(f"{get_retry_path()}")
        logging.debug(f"Saving retry config: [{title}]")
        chapters_json = list(map(lambda x: x.to_json(), chapters)) 
        with open(f"{get_retry_path()}/{title}.json", "w+") as outfile:
            json.dump(chapters_json, outfile)
        pass
    except Exception as e:
        logging.error(f"unable to save retry config: {e}")


def save_download_config() -> None:
    return


def get_download_config() -> list[dict]:
    return

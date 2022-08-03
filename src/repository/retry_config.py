import os
import json
import logging

def get_retry_path():
    return "/config/retry"
    
def get_retry_config(file_name):
    try:
        logging.debug(f"Getting {file_name} retry config")
        json_file = open(f"{get_retry_path()}/{file_name}.json", "r")
        retry_json = json.load(json_file)
        json_file.close()
        logging.debug(f"Deleting {file_name} retry config")
        os.remove(file_path)
        return (retry_json["title"], retry_json["chapters"])
    except:
        return []    

def save_retry_config(title, chapters):
    try:
        if(not os.path.exists(get_retry_path())):
            logging.debug(f"Add missing retry config dir")
            os.makedirs(f"{get_retry_path()}")
        logging.debug(f"Saving retry config: [{title}]")    
        with open(f"{get_retry_path()}/{title}.json", "w+") as outfile:
            json_dump = {
                "title": title,
                "chapters": chapters
            }
            json.dump(json_dump, outfile)
        pass
    except Exception as e: 
        logging.error(f"unable to save retry config: {e}")       


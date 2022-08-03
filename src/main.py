from utils.logger import logger 
from service.downloader import Downloader
from service.retry_service import retry_from_config

def dowload_all(goto_url):
    Downloader().dowload_all_chapters(goto_url)

def dowload_one(title, goto_url):
    Downloader().dowload_one_chapters(title, goto_url)    

# def find_missing_chapter():   
#     files = list(map(lambda s: int(s.name.replace("Black Clover chapter ", "").replace(".png", "")), os.scandir("./Black Clover")))
#     files.sort()
#     count = 1
#     for filename in files:
#         if(not count == filename):
#               print(filename - 1)     
#               break     
#         count += 1 
#     pass

# TODO add arguments instead of manually changing got_url
if __name__ == "__main__":
    dowload_all("")
    # retry_from_config()
    pass





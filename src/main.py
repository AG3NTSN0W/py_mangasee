import re
import argparse
from utils.logger import logger 
from service.downloader import Downloader
from service.retry_service import retry_from_config

def validateUrl(pattern, value):
    return re.match(pattern, value)

def start(args):
    pool = args.pool
    format = args.format
    url = args.url
    splite = args.splite

    downloader = Downloader(splite, pool, format)

    if (url and validateUrl("https:\/\/mangasee123\.com\/rss\/.*\.xml", url)):
        downloader.dowload_all_chapters(url)
        return
    
    if (url and validateUrl("https:\/\/mangasee123\.com\/read-online\/.*\.html", url)):
        downloader.dowload_one_chapters(url)
        return

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='')

    parser.add_argument(
            '-u',
            '--url',
            help='Url of manga chapter to download or RSS of the manga to download'
    )

    parser.add_argument(
        '-f',
        '--format',
        help='File formate to save in pdf | png',
        default='pdf'
    )    

    parser.add_argument(
        '-p',
        '--pool',
        help='Pool size',
        type=int,
        default=2
    )    

    parser.add_argument(
        '-s',
        '--splite',
        help='Save all image into separate file',
        action='store_true',
        default=False
    )    
    
    
    start(parser.parse_args())
    pass





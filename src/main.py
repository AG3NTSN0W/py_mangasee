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
    chapter = args.chapter

    downloader = Downloader(splite, pool, format)

    if (not url and not validateUrl("https:\/\/mangasee123\.com\/rss\/.*\.xml", url)):
        return

    if(chapter):
        downloader.dowload_chapter(url, chapter)
        return

    downloader.dowload_all_chapters(url)

def arguments():
    parser = argparse.ArgumentParser(description='')

    parser.add_argument(
        '-u',
        '--url',
        help='RSS of the manga to download'
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

    parser.add_argument(
        '-c',
        '--chapter',
        help='Chapter number',
    )
    return parser

if __name__ == "__main__":
    
    # start(arguments().parse_args())
    retry_from_config()
    pass

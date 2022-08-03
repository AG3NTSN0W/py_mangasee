
import logging

FORMAT = '%(asctime)s | %(levelname)s | [%(filename)s] - %(message)s'

logging.basicConfig(filename='app.log',
    filemode='w',
    format=FORMAT,
    level=logging.INFO,
    datefmt='%m/%d/%Y %H:%M:%S'
)

logger = logging.getLogger()

    

import logging
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

from utils.logger import logger 


def get_driver():
    EXECUTABLE_PATH = "/usr/bin/geckodriver"
    
    # FireFox PROFILE
    PROFILE = webdriver.FirefoxProfile()
    PROFILE.set_preference("browser.cache.disk.enable", False)
    PROFILE.set_preference("browser.cache.memory.enable", False)
    PROFILE.set_preference("browser.cache.offline.enable", False)
    PROFILE.set_preference("network.http.use-cache", False)
    
    # FireFox Options
    FIREFOX_OPTS = Options()
    FIREFOX_OPTS.log.level = "trace"    # Debug
    FIREFOX_OPTS.headless = True
    GECKODRIVER_LOG = '/geckodriver.log'
    ff_opt = {
		"firefox_profile": PROFILE,
		"options": FIREFOX_OPTS,
		"service_log_path": GECKODRIVER_LOG,
        "executable_path": EXECUTABLE_PATH
	}
    return webdriver.Firefox(**ff_opt)

def get_manga_images(goto_url):
    try:
        logger.debug(f"Getting all images from: [{goto_url}]")
        driver = get_driver()
        driver.get(goto_url)
        page_content = driver.page_source
        driver.quit()
        logger.debug(f"Web drive Closed")
        imgContainers = BeautifulSoup(page_content, 'html.parser').find(id="TopPage").findAll("img", class_="img-fluid")
        return list(map(lambda x: x['src'], imgContainers))
    except Exception as e:
        raise WebScraperException("web_scraper", e)
    
class WebScraperException(Exception):
    def __init__(self, service, error):
        # Call the base class constructor with the parameters it needs
        super(Exception, self).__init__(service, error)  

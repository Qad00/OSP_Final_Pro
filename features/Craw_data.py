#!/usr/bin/python3

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import csv

class Craw_data:
    def __init__(self):
        chrome_driver = ChromeDriverManager().install()
        service = Service(chrome_driver)
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        
        self.driver = webdriver.Chrome(service=service, options=options)
        self.craw_result = dict()
    
    def getTitle(self, keyword, url='https://www.youtube.com/'):
        if len(keyword) > 0:
            self.craw_result[keyword] = dict()

            self.driver.get(url)
            time.sleep(3)

            # Crawling start...

            self.driver.close()
    
    def getComments(self, link):
        self.driver.get(link)
        time.sleep(3)

        # Crawling start...

        self.driver.close()
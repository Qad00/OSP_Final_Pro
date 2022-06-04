#!/usr/bin/python3
#-*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from tqdm import tqdm

class Craw_data:
    def __init__(self):
        chrome_driver = ChromeDriverManager().install()
        service = Service(chrome_driver)
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        
        self.driver = webdriver.Chrome(service=service, options=options)

    def setHVideo(self, url='https://www.youtube.com/'):
        '''
            Structure of "hVideo"
            {
                "{Video Link1}" : {
                    "title" : "{Video Title}",
                    "img" : "{Video Thumbnail Image Link}",
                    "hits" : "{Video Hits}",
                    "likes" : "{Video Likes}"
                },
                "{Video Link2}" : {
                    "title" : "{Video Title}",
                    "img" : "{Video Thumbnail Image Link}",
                    "hits" : "{Video Hits}",
                    "likes" : "{Video Likes}"
                },
                ...
            }
        '''
        self.hVideo = dict()    # Store Home Videos Information 

        self.driver.maximize_window()
        self.driver.get(url)
        time.sleep(3)

        # Crawling start...
        imgs = self.driver.find_elements(By.CSS_SELECTOR, "ytd-rich-grid-row div#content a#thumbnail img#img")
        time.sleep(2)

        titles = self.driver.find_elements(By.CSS_SELECTOR, "ytd-rich-grid-row yt-formatted-string#video-title")
        time.sleep(2)

        links = self.driver.find_elements(By.CSS_SELECTOR, "ytd-rich-grid-row a#video-title-link")
        time.sleep(2)
        
        print('Part 1. Title, Image Crawling')
        for idx in tqdm(range(10)):
            link = links[idx].get_attribute('href')
            self.hVideo[link] = dict()
            self.hVideo[link]['title'] = titles[idx].text
            self.hVideo[link]['img'] = imgs[idx].get_attribute('src')

        print('Part 2. Hits, Like Crawling')
        for link in tqdm(self.hVideo.keys()):
            # 조회수, 좋아요 수 추출
            self.driver.get(link)
            time.sleep(3)

            hits = self.driver.find_element(By.CSS_SELECTOR, 'div#info ytd-video-view-count-renderer span.view-count.style-scope.ytd-video-view-count-renderer').text
            time.sleep(2)
            likes = self.driver.find_element(By.CSS_SELECTOR, 'div#menu-container a.yt-simple-endpoint.style-scope.ytd-toggle-button-renderer yt-formatted-string#text').text
            time.sleep(2)

            self.hVideo[link]['hits'] = hits
            self.hVideo[link]['likes'] = likes

    def getHVideo(self):
        return self.hVideo

    def setKVideo(self, keyword, url='https://www.youtube.com/'):
        '''
            Structure of "kVideo"
            {
                "{keyword}" : {
                    "{Video Link1}" : {
                        "title" : "{Video Title}",
                        "img" : "{Video Thumbnail Image}",
                        "hits" : "{Video Hits}",
                        "likes" : "{Video Likes}"
                    },
                    "{Video Link2}" : {
                        "title" : "{Video Title}",
                        "img" : "{Video Thumbnail Image}",
                        "hits" : "{Video Hits}",
                        "likes" : "{Video Likes}"
                    },
                    ...
                },
                "{keyword}" : {
                    "{Video Link1}" : {
                        "title" : "{Video Title}",
                        "img" : "{Video Thumbnail Image}",
                        "hits" : "{Video Hits}",
                        "likes" : "{Video Likes}"
                    },
                    "{Video Link2}" : {
                        "title" : "{Video Title}",
                        "img" : "{Video Thumbnail Image}",
                        "hits" : "{Video Hits}",
                        "likes" : "{Video Likes}"
                    },
                    ...
                },
                ...
            }
        '''
        if len(keyword) > 0:
            self.kVideo = dict()    # Store Videos Information about the keyword
            self.kVideo[keyword] = dict()

            self.driver.maximize_window()
            self.driver.get(url)
            time.sleep(3)

            # Crawling start...
            self.driver.find_element(By.CSS_SELECTOR, "input#search").clear()
            time.sleep(1)
            self.driver.find_element(By.CSS_SELECTOR, "input#search").send_keys(keyword)
            time.sleep(2)
            self.driver.find_element(By.CSS_SELECTOR, "button#search-icon-legacy").click()
            time.sleep(2)
            
            imgs = self.driver.find_elements(By.CSS_SELECTOR, "ytd-video-renderer a#thumbnail img#img")
            time.sleep(2)

            titles = self.driver.find_elements(By.CSS_SELECTOR, "#video-title > yt-formatted-string")
            time.sleep(2)

            links = self.driver.find_elements(By.CSS_SELECTOR, "ytd-video-renderer a#video-title")
            time.sleep(2)
            
            print('Part 1. Title, Image Crawling')
            for idx in tqdm(range(10)):
               link = links[idx].get_attribute('href')
               self.kVideo[keyword][link] = dict()
               self.kVideo[keyword][link]['title'] = titles[idx].text
               self.kVideo[keyword][link]['img'] = imgs[idx].get_attribute('src')
              
            print('Part 2. Hits, Like Crawling')
            for link in tqdm(self.kVideo[keyword].keys()):
                # 조회수, 좋아요 수 추출
                self.driver.get(link)
                time.sleep(3)

                hits = self.driver.find_element(By.CSS_SELECTOR, 'div#info ytd-video-view-count-renderer span.view-count.style-scope.ytd-video-view-count-renderer').text
                time.sleep(2)
                likes = self.driver.find_element(By.CSS_SELECTOR, 'div#menu-container a.yt-simple-endpoint.style-scope.ytd-toggle-button-renderer yt-formatted-string#text').text
                time.sleep(2)

                self.kVideo[keyword][link]['hits'] = hits
                self.kVideo[keyword][link]['likes'] = likes
        else:
            print("No Keyword...")
    
    def getKVideo(self):
        return self.kVideo

    def setVComment(self, link, sc_num=60):
        '''
            Structure of "vComment"
            {
                "{Video Link}" : [{댓글1}, {댓글2}, ...]
            }
        '''
        self.vComment = dict()   # Store Comments of a Video
        self.vComment[link] = []

        self.driver.set_window_size(1020,1020)
        self.driver.get(link)
        time.sleep(3)

        # Crawling start...
        # 페이지 맨 밑으로 내리기 (sc_num만큼)
        print("Scrolling...")
        scroll_count = 0
        while scroll_count < sc_num:
            scroll_position = 10000 + scroll_count * 10000
            self.driver.execute_script(f"window.scrollTo(0,{scroll_position});")
            time.sleep(1)

            scroll_count += 1
        
        print("Comment Finding...")
        comments = self.driver.find_elements(By.CSS_SELECTOR,'yt-formatted-string#content-text')
        time.sleep(2)

        for comment in comments:
            self.vComment[link].append(comment.text)

    def getVComment(self):
        return self.vComment

    def closeDriver(self):
        self.driver.close()

if __name__=="__main__":
    # Test
    print()

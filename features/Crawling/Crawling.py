#!/usr/bin/python
#-*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
from tqdm import tqdm

class Crawling:
    def __init__(self):
        chrome_driver = ChromeDriverManager().install()
        service = Service(chrome_driver)
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--window-size=1920x1080')
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
        print('Part 1. Title, Image Crawling')
        with tqdm(total=10) as pbar:
            idx = 0
            while(len(self.hVideo.keys()) < 10):
                # 실시간 영상 제외
                if(self.driver.find_element(By.XPATH, f'/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-rich-grid-renderer/div[6]/ytd-rich-grid-row[{idx // 4 + 1}]/div/ytd-rich-item-renderer[{idx % 4 + 1}]/div/ytd-rich-grid-media/div[1]/div[2]/div[1]/ytd-badge-supported-renderer[1]').text == ''):
                    time.sleep(2)
                    link = self.driver.find_element(By.XPATH, f'/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-rich-grid-renderer/div[6]/ytd-rich-grid-row[{idx // 4 + 1}]/div/ytd-rich-item-renderer[{idx % 4 + 1}]/div/ytd-rich-grid-media/div[1]/div[2]/div[1]/h3/a').get_attribute('href')
                    time.sleep(1)
                    img = self.driver.find_element(By.XPATH, f'/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-rich-grid-renderer/div[6]/ytd-rich-grid-row[{idx // 4 + 1}]/div/ytd-rich-item-renderer[{idx % 4 + 1}]/div/ytd-rich-grid-media/div[1]/ytd-thumbnail/a/yt-img-shadow/img').get_attribute('src')
                    time.sleep(1)
                    title = self.driver.find_element(By.XPATH, f'/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-rich-grid-renderer/div[6]/ytd-rich-grid-row[{idx // 4 + 1}]/div/ytd-rich-item-renderer[{idx % 4 + 1}]/div/ytd-rich-grid-media/div[1]/div[2]/div[1]/h3/a/yt-formatted-string').text
                    time.sleep(1)

                    self.hVideo[link] = dict()
                    self.hVideo[link]['title'] = title
                    self.hVideo[link]['img'] = img

                    pbar.update(1)
                idx += 1

        print('Part 2. Hits, Like Crawling')
        for link in tqdm(self.hVideo.keys()):
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
            
            print('Part 1. Title, Image Crawling')
            with tqdm(total=10) as pbar:
                idx = 0
                while(len(self.kVideo[keyword].keys()) < 10):
                    # 실시간 영상 제외
                    if('실시간' not in self.driver.find_element(By.XPATH,f'/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer[1]/div[3]/ytd-video-renderer[{idx + 1}]/div[1]/div/ytd-badge-supported-renderer').text):
                        time.sleep(1)
                        link = self.driver.find_element(By.XPATH, f'/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[{idx + 1}]/div[1]/ytd-thumbnail/a').get_attribute('href')
                        time.sleep(1)
                        img = self.driver.find_element(By.XPATH, f'/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[{idx + 1}]/div[1]/ytd-thumbnail/a/yt-img-shadow/img').get_attribute('src')
                        time.sleep(1)
                        title = self.driver.find_element(By.XPATH, f'/html/body/ytd-app/div[1]/ytd-page-manager/ytd-search/div[1]/ytd-two-column-search-results-renderer/div/ytd-section-list-renderer/div[2]/ytd-item-section-renderer/div[3]/ytd-video-renderer[{idx + 1}]/div[1]/div/div[1]/div/h3/a/yt-formatted-string').text
                        time.sleep(1)

                        self.kVideo[keyword][link] = dict()
                        self.kVideo[keyword][link]['title'] = title
                        self.kVideo[keyword][link]['img'] = img
                        
                        pbar.update(1)
                    idx += 1
  
            print('Part 2. Hits, Like Crawling')
            for link in tqdm(self.kVideo[keyword].keys()):
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
        print("Page Scrolling...")
        with tqdm(total=sc_num) as pbar:
            scroll_count = 0
            while scroll_count < sc_num:
                scroll_position = 10000 + scroll_count * 10000
                self.driver.execute_script(f"window.scrollTo(0,{scroll_position});")
                time.sleep(1)

                pbar.update(1)
                scroll_count += 1
        
        print("Comment Finding...")
        comments = self.driver.find_elements(By.CSS_SELECTOR,'yt-formatted-string#content-text')
        time.sleep(2)

        print("Comment Storing...")
        for comment in tqdm(comments):
            self.vComment[link].append(comment.text)

    def getVComment(self):
        return self.vComment

    def closeDriver(self):
        print("Driver Closing...")
        self.driver.quit()

if __name__=="__main__":
    # Test
    print()

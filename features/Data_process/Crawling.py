#!/usr/bin/python
#-*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
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
        
        # Crawling Start...
        print('Part 1. Title, Image, Link Crawling')
        html = self.driver.page_source
        bs = BeautifulSoup(html,'html.parser')
        rowVideos = bs.find_all('ytd-rich-grid-row')

        with tqdm(total=10) as pbar:
            idx = 0
            while(len(self.hVideo.keys()) < 10):
                videos = rowVideos[idx].find_all('ytd-rich-item-renderer')
                for subIdx in range(len(videos)):
                    # 영상 Crawling...
                    if(len(self.hVideo.keys()) < 10):
                        # 실시간 영상 제외
                        if(videos[subIdx].find_all('ytd-badge-supported-renderer')[2].text.strip() == ''):
                            # print(f'[{subIdx}]')
                            title = videos[subIdx].find('yt-formatted-string').text.strip()
                            # print(title)
                            link = videos[subIdx].select('a#video-title-link')[0].attrs['href']
                            # print(link)
                            if('src' in videos[subIdx].select('img#img')[0].attrs.keys()):
                                img = videos[subIdx].select('img#img')[0].attrs['src']
                            else:
                                img = None
                            # print(img)

                            self.hVideo[f'{url}{link}'] = dict()
                            self.hVideo[f'{url}{link}']['title'] = title
                            self.hVideo[f'{url}{link}']['img'] = img

                            pbar.update(1)
                idx += 1

        print('Part 2. Hits, Like Crawling')
        for link in tqdm(self.hVideo.keys()):
            self.driver.get(link)
            time.sleep(3)

            html = self.driver.page_source
            bs = BeautifulSoup(html,'html.parser')

            hits = bs.select('#count > ytd-video-view-count-renderer > span.view-count.style-scope.ytd-video-view-count-renderer')[0].text
            # print(hits)
            likes = bs.select('yt-formatted-string#text.style-scope.ytd-toggle-button-renderer.style-text')[0].text
            # print(likes)

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

            self.driver.find_element(By.CSS_SELECTOR, "input#search").clear()
            time.sleep(1)
            self.driver.find_element(By.CSS_SELECTOR, "input#search").send_keys(keyword)
            time.sleep(2)
            self.driver.find_element(By.CSS_SELECTOR, "button#search-icon-legacy").click()
            time.sleep(2)
            
            # Crawling start...
            html = self.driver.page_source
            bs = BeautifulSoup(html, 'html.parser')
            videos = bs.find_all('ytd-video-renderer')
                
            print('Part 1. Title, Image Link Crawling')
            with tqdm(total=10) as pbar:
                idx = 0
                while(len(self.kVideo[keyword].keys()) < 10):
                    # 실시간 영상 제외
                    if(videos[idx].select('#badges > div.badge.badge-style-type-live-now-alternate.style-scope.ytd-badge-supported-renderer') == []):
                        # print(f'[{idx}]')
                        title = videos[idx].select('#video-title > yt-formatted-string')[0].text.strip()
                        # print(title)
                        link = videos[idx].select('a#video-title')[0].attrs['href']
                        # print(link)
                        if('src' in videos[idx].select('img#img')[0].attrs.keys()):
                            img = videos[idx].select('img#img')[0].attrs['src']
                        else:
                            img = None
                        # print(img)
                        
                        self.kVideo[keyword][f'{url}{link}'] = dict()
                        self.kVideo[keyword][f'{url}{link}']['title'] = title
                        self.kVideo[keyword][f'{url}{link}']['img'] = img

                        pbar.update(1)
                    idx += 1
  
            print('Part 2. Hits, Like Crawling')
            for link in tqdm(self.kVideo[keyword].keys()):
                self.driver.get(link)
                time.sleep(3)

                html = self.driver.page_source
                bs = BeautifulSoup(html,'html.parser')

                hits = bs.select('#count > ytd-video-view-count-renderer > span.view-count.style-scope.ytd-video-view-count-renderer')[0].text
                # print(hits)
                likes = bs.select('yt-formatted-string#text.style-scope.ytd-toggle-button-renderer.style-text')[0].text
                # print(likes)

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
        self.vComment[link] = list()

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
    print('Testing Start...')
    # ...

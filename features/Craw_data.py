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
        #options.add_argument('--headless')
        #options.add_argument('--no-sandbox')
        #options.add_argument('--disable-dev-shm-usage')
        options.add_experimental_option("excludeSwitches", ["enable-logging"])
        
        self.driver = webdriver.Chrome(service=service, options=options)
        
    def setHVideo(self, url='https://www.youtube.com/'):
        '''
            Structure of "hVideo"
            {
                "{Video Link1}" : {
                    "title" : "{Video Title}",
                    "img" : "{Video Thumbnail Image Link}"
                },
                "{Video Link2}" : {
                    "title" : "{Video Title}",
                    "img" : "{Video Thumbnail Image Link}"
                },
                ...
            }
        '''
        self.hVideo = dict()    # Store Home Videos Information 

        self.driver.get(url)
        time.sleep(3)

        # Crawling start...
        imgs = self.driver.find_elements(By.CSS_SELECTOR, "ytd-rich-grid-row div#content a#thumbnail img#img")
        time.sleep(2)

        titles = self.driver.find_elements(By.CSS_SELECTOR, "ytd-rich-grid-row yt-formatted-string#video-title")
        time.sleep(2)

        links = self.driver.find_elements(By.CSS_SELECTOR, "ytd-rich-grid-row a#video-title-link")
        time.sleep(2)
        
        for idx in range(10):
            link = links[idx].get_attribute('href')
            self.hVideo[link] = dict()
            self.hVideo[link]['title'] = titles[idx].text
            self.hVideo[link]['img'] = imgs[idx].get_attribute('src')
        
        self.driver.close()

    def getHVideo(self):
        return self.hVideo

    def setKVideo(self, keyword, url='https://www.youtube.com/'):
        '''
            Structure of "kVideo"
            {
                "{keyword}" : {
                    "{Video Link1}" : {
                        "title" : "{Video Title}",
                        "img" : "{Video Thumbnail Image}"
                    },
                    "{Video Link2}" : {
                        "title" : "{Video Title}",
                        "img" : "{Video Thumbnail Image}"
                    },
                    ...
                },
                "{keyword}" : {
                    "{Video Link1}" : {
                        "title" : "{Video Title}",
                        "img" : "{Video Thumbnail Image}"
                    },
                    "{Video Link2}" : {
                        "title" : "{Video Title}",
                        "img" : "{Video Thumbnail Image}"
                    },
                    ...
                },
                ...
            }
        '''
        if len(keyword) > 0:
            self.kVideo = dict()    # Store Videos Information about the keyword
            self.kVideo[keyword] = dict()

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
            
            for idx in tqdm(range(10)):
                link = links[idx].get_attribute('href')
                self.kVideo[keyword][link] = dict()
                self.kVideo[keyword][link]['title'] = titles[idx].text
                self.kVideo[keyword][link]['img'] = imgs[idx].get_attribute('src')

            #self.driver.close()
        else:
            print("No Keyword...")
    
    def getKVideo(self):
        return self.kVideo

    def setVComment(self, link):
        self.vComment = dict()   # Store Comments of a Video
        self.vComment[link] = dict()

        self.driver.get(link)
        time.sleep(3)

        # Crawling start...

        self.driver.close()

    def getVComment(self):
        return self.vComment

if __name__=="__main__":
    crawData = Craw_data()
    crawData.setKVideo(keyword='rap')
    print(crawData.getKVideo())
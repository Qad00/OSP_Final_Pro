#!/usr/bin/python
#-*- coding: utf-8 -*-
# 필요한 library 가져오기
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import time
import csv

'''
    This code is sample code to crawl title of Youtube video.
    Running on Local Environment.
'''

# 유튜브 웹 페이지 접속
# 자동화된 크롬 창 실행
chrome_driver = ChromeDriverManager().install()
service = Service(chrome_driver)
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(service=service, options=options)

# 유튜브 웹 페이지 접속
yt_url = 'https://www.youtube.com/'
driver.get(yt_url)

# 시간적 여유 3초
time.sleep(3)

# 검색한 페이지의 동영상 제목 가져오기
def return_result(keyword):
    # 검색창에 단어 입력
    driver.find_element(By.CSS_SELECTOR, "input#search").clear()
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, "input#search").send_keys(keyword)
    time.sleep(2)
    driver.find_element(By.CSS_SELECTOR, "button#search-icon-legacy").click()
    time.sleep(2)

    # 검색 결과 저장
    output = []
    scroll_count = 0
    while scroll_count <= 10:
        target = driver.find_elements(By.CSS_SELECTOR, "a#video-title yt-formatted-string,style-scope ytd-video-renderer")
        time.sleep(2)

        for item in target:
            if item.text not in output:
                output.append(item.text)
        time.sleep(2)
        print("Done.")
        scroll_position = 900 + scroll_count * 900
        driver.execute_script(f"window.scrollTo(0,{scroll_position});")
        time.sleep(2)

        scroll_count += 1
    
    return output

# CSV 파일 'youtube_title.csv' 생성
# 작성할 'youtube_title.csv' 파일을 생성하여 변수 'f'에 저장
f = open('./youtube_title.csv', 'w', newline = '', encoding='utf-8')

# writer 객체 생성 & 파일의 열 제목 생성
# CSV 파일을 작성하는 객체 변수 'wtr' 생성
wtr = csv.writer(f)
# 열 제목 작성
wtr.writerow(['Youtube 영상 제목'])

# list 생성
yt_title = []

# 반복문을 활용하여 번역기 구현 및 CSV 파일에 저장
# 무한 루프
while True:
    keyword = input("검색할 영상의 제목 입력 ('0' 입력하면 종료, 'check' 입력하면 현재 크롤링한 영상 제목 결과 확인) : ")
    if keyword == "0":
        print("크롤링 종료")
        break
    elif keyword == 'check':
        for title in yt_title:
            print(title)
    else:
        # youtube_title.csv 파일에 [영상 제목] 작성
        for title in return_result(keyword):
            wtr.writerow([title])
            yt_title.append(title)

driver.close()
f.close()
#-*- coding: utf-8 -*-
# 필요한 library 가져오기
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import csv

# 유튜브 웹 페이지 접속
# 자동화된 크롬 창 실행
chrome_driver = ChromeDriverManager().install()
service = Service(chrome_driver)
options = webdriver.ChromeOptions()
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
    driver.find_element(By.CSS_SELECTOR, "input#search").send_keys(keyword)
    driver.find_element(By.CSS_SELECTOR, "button#search-icon-legacy").click()
    time.sleep(1)

    # 검색 결과 저장
    target = driver.find_elements(By.CSS_SELECTOR, "a#video-title yt-formatted-string,style-scope ytd-video-renderer")
    time.sleep(2)

    output = []
    for item in target:
        if item.text not in output:
            output.append(item.text)
        time.sleep(1)
    
    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
    time.sleep(2)

    target = driver.find_elements(By.CSS_SELECTOR, "a#video-title yt-formatted-string,style-scope ytd-video-renderer")
    time.sleep(2)

    for item in target:
        if item.text not in output:
            output.append(item.text)
        time.sleep(1)
    
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
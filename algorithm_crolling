import random
import time
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import re

# 웹 드라이버 설정
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # 화면을 표시하지 않음
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)

# 무신사 남성 인기 랭킹 페이지로 이동
url = 'https://www.musinsa.com/ranking/best?gender=m'
driver.get(url)
time.sleep(3)  # 페이지 로딩 대기

# 페이지 소스 가져오기
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')

# 상의와 하의 항목 찾기
items = soup.select('li.sc-1m4cyao-1.dYjLwF')

# 각 항목의 링크 추출하여 리스트에 저장
item_links = []
for item in items:
    link_tag = item.select_one('a.sc-1m4cyao-2.bubXVJ.gtm-select-item')  # 링크가 포함된 태그 선택
    if link_tag:
        item_link = link_tag['href']  # href 속성 가져오기
        item_links.append(item_link)  # 리스트에 링크 추가

# 웹 드라이버 종료
driver.quit()

# 상의와 하의 각각 랜덤 선택
if item_links:
    top_link = random.choice(item_links)
    bottom_link = random.choice(item_links)
    print(f"추천 상의 링크: {top_link}")
    print(f"추천 하의 링크: {bottom_link}")
else:
    print("항목을 찾을 수 없습니다.")

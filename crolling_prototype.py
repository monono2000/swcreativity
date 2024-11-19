import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# 웹 드라이버 설정
options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)

# 무신사 남성 인기 랭킹 페이지로 이동
url = 'https://www.musinsa.com/main/musinsa/recommend?gf=M'
driver.get(url)
time.sleep(3)

# 팝업 배너 닫기
try:
    driver.find_element(By.XPATH, '/html/body/section/div[2]/button').click()
except Exception:
    print("팝업 배너가 없거나 이미 닫혔습니다.")

# 전체->남성으로 변경 버튼 클릭
driver.find_element(By.XPATH, '//*[@id="commonLayoutFab"]/div/div/div/button[1]').click()
driver.find_element(By.XPATH, '//*[@id="commonLayoutFab"]/div/div/div/button[2]').click()
time.sleep(3)

# 검색어 입력 함수
def search_product(keyword):
    driver.find_element(By.XPATH, '//*[@id="commonLayoutHeader"]/section/div[2]/div/button[1]').click()
    search_box = driver.find_element(By.XPATH, '//*[@id="commonSearchHome"]/main/header/div/input')
    search_box.send_keys(keyword)
    search_box.send_keys(Keys.RETURN)
    time.sleep(2)

# 페이지 스크롤 함수
def scroll_page(scroll_times=10):
    for _ in range(scroll_times):
        driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)
        time.sleep(1)

# 데이터 크롤링 함수
def scrape_data():
    data_list = []
    max_j = 39  # j의 최대값 설정
    max_i = 3   # i의 최대값 설정
    
    for j in range(1, max_j + 1):
        for i in range(1, max_i + 1):
            xpath = f'//*[@id="commonLayoutContents"]/div/div[4]/div/div/div/div[{j}]/div/div[{i}]'
            try:
                # 동적 XPATH를 이용하여 데이터 찾기
                element = driver.find_element(By.XPATH, xpath)
                product_text = element.text.strip()
                
                # 줄바꿈으로 텍스트 나누기
                product_info = product_text.split("\n")
                
                # 제품 정보가 충분한 경우에만 처리
                if len(product_info) >= 9:
                    brand = product_info[0]  # 브랜드
                    name = product_info[1]   # 제품명
                    discount = product_info[2]  # 할인율
                    price = product_info[3]   # 가격
                    gender = product_info[9]  # 성별 (남성/여성 등)

                    # 정보를 리스트로 추가
                    data_list.append([brand, name, discount, price, gender])
            except Exception as e:
                print(f"Error at index [{j}, {i}]: {e}")
    
    return data_list


# 사용자로부터 검색 키워드 입력받기
search_keyword = input("검색할 키워드를 입력하세요: ")  # 사용자 정의 검색어 입력
search_product(search_keyword)
scroll_page(scroll_times=20)
data = scrape_data()


# DataFrame 생성 (각 항목을 열로 나누기)
df = pd.DataFrame(data, columns=['브랜드', '제품명', '할인율', '가격', '성별'])

# CSV로 저장
df.to_csv('musinsa_data.csv', index=False, encoding='utf-8-sig')
print("데이터가 'musinsa_data.csv'로 저장되었습니다.")



# 드라이버 종료
driver.quit()

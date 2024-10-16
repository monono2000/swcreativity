#create by 김태훈

# 무신사 남성 인기 랭킹 페이지로 이동
url = 'https://www.musinsa.com/main/musinsa/ranking?gf=M' # CHK: 오류가 있을때는 HEADLESS 제거후 눈으로 보면서 확인
driver.get(url)
time.sleep(3)  # 페이지 로딩 대기

driver.find_element(By.XPATH, '/html/body/section/div[2]/button').click()

# 페이지 소스 가져오기
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')

# 페이지를 아래로 3번 스크롤
for _ in range(3):
    # JavaScript를 사용하여 페이지의 끝까지 스크롤
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    
    # 데이터 로드 시간을 고려하여 잠시 대기 (웹사이트에 따라 조정)
    time.sleep(2)

from selenium.webdriver.common.by import By
temp = driver.find_element(By.XPATH, '//*[@id="commonLayoutContents"]/article/div[3]') 


# 빈 리스트 생성 (크롤링한 데이터를 저장할 공간)
data_list = []

# 반복문을 사용하여 2부터 40까지 반복
for j in range(2, 40):
    for i in range(1, 4):
        # XPATH에서 인덱스를 적용하여 동적으로 XPATH를 변경
        xpath = f'//*[@id="commonLayoutContents"]/article/div[{j}]/div[{i}]'

        try:
            # 해당 XPATH를 이용해 요소 찾기
            element = driver.find_element(By.XPATH, xpath)
            
            # 찾은 요소의 텍스트를 리스트에 추가 (또는 필요한 데이터를 추출)
            data_list.append(element.text)
            
        except Exception as e:
            print(f"Error at index [{j}, {i}]: {e}")

# 크롤링한 데이터를 pandas DataFrame으로 변환
df = pd.DataFrame(data_list, columns=['Data'])

# 데이터를 \n 기준으로 분리하여 DataFrame 생성
# 각 데이터를 \n으로 분리한 후 리스트로 만듭니다.
split_data = [item.split('\n') for item in data_list]

# DataFrame으로 변환하고 열 이름 설정
df = pd.DataFrame(split_data, columns=['Rank', 'Brand', 'Discount', 'Price', 'Viewers'])

# 데이터를 'data.csv' 파일로 저장
df.to_excel('data.csv', index=False, encoding='utf-8-sig')

# 저장하는 과정에서 오류 다수 발생
print("데이터 저장 완료")


# 밑 사항들은 점차 구현해야 함
temp2 = temp.find_element(By.TAG_NAME, "img")
temp2.get_attribute('href')

# js에서 응답을 주면 파이썬을 실행하는 코드를 추가해야 함
# code by 김태훈

import os
import pandas as pd
import random
import time
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import csv
import json
from urllib.parse import urljoin, urlparse, parse_qs
import shutil
from selenium.common.exceptions import NoSuchElementException, ElementNotInteractableException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def preprocess_json(line):
    # JSON 데이터 내 Key/Value가 올바르게 감싸지도록 전처리
    line = re.sub(r'([{,])(\s*)([a-zA-Z_][a-zA-Z0-9_]*)(\s*):', r'\1"\3":', line)  # Key에 쌍따옴표 추가
    line = re.sub(r'(?<=:)(\s*)([a-zA-Z_]+)(\s*)([,}])', r'\1"\2"\3\4', line)  # Value에 쌍따옴표 추가
    return line

def extract_logs_to_csv(log_file_path, csv_file_path):
    recommendations = []
    sizes = {}
    colors = []

    with open(log_file_path, mode='r', encoding='utf-8') as file:
        for line in file:
            try:
                if 'Outfit Recommendations Success' in line:
                    start_index = line.find('[')
                    end_index = line.rfind(']') + 1
                    if start_index != -1 and end_index != -1:
                        data = preprocess_json(line[start_index:end_index])
                        recommendations = json.loads(data)

                elif 'Get Size Info Success' in line:
                    start_index = line.find('{')
                    end_index = line.rfind('}') + 1
                    if start_index != -1 and end_index != -1:
                        data = line[start_index:end_index]
                        sizes = json.loads(data)

                elif 'Color Matching Success' in line:
                    start_index = line.find('[')
                    end_index = line.rfind(']') + 1
                    if start_index != -1 and end_index != -1:
                        data = preprocess_json(line[start_index:end_index])
                        colors = json.loads(data)
            except json.JSONDecodeError as e:
                print(f"JSON 디코딩 실패: {e}, 데이터: {line}")

    # CSV 파일 저장
    with open(csv_file_path, mode='w', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        
        # Header 작성
        csvwriter.writerow(['Outerwear', 'Top', 'Bottom', 'Outer Size', 'Top Size', 'Outer Color', 'Top Color', 'Bottom Color'])

        # 데이터 작성
        for i, rec in enumerate(recommendations):
            outerwear = rec.get('outerwear', 'NULL')
            top = rec.get('top', 'NULL')
            bottom = rec.get('bottom', 'NULL')
            
            outer_size = sizes.get('outer_size', 'NULL')
            top_size = sizes.get('top_size', 'NULL')

            outer_color = colors[i].get('outer_color', 'NULL') if i < len(colors) else 'NULL'
            top_color = colors[i].get('top_color', 'NULL') if i < len(colors) else 'NULL'
            bottom_color = colors[i].get('bottom_color', 'NULL') if i < len(colors) else 'NULL'

            csvwriter.writerow([outerwear, top, bottom, outer_size, top_size, outer_color, top_color, bottom_color])

# 실행
log_file_path = "logs.csv"
csv_file_path = "recommendations.csv"
extract_logs_to_csv(log_file_path, csv_file_path)


# 색상 변환 딕셔너리
color_translation = {
    'White': '화이트',
    'Gray': '그레이',
    'Black': '블랙',
    'Blue': '블루',
    'Navy': '네이비',
    'Denim': '데님',
    'Olive': '올리브 그린',
    'Khaki': '카키',
    'Ivory': '아이보리',
    'Beige': '베이지',
    'Brown': '브라운',
}

# CSV 파일 경로 설정
input_csv = 'recommendations.csv'  # 입력 CSV 파일 경로
csv_file_path = 'recommendations_io.csv'  # 출력 CSV 파일 경로

# CSV 파일 읽기
df = pd.read_csv(input_csv)

# 색상 컬럼에 대해 한글로 변환
def translate_color(color):
    # 색상이 딕셔너리에 존재하면 변환하고, 아니면 원래 색상 반환
    if isinstance(color, str):
        return color_translation.get(color.strip(), color)  # 공백 제거 후 변환
    return color

# 'null' 문자열과 빈 문자열('')을 'NULL'로 변환
def convert_empty_to_null(value):
    if value == '' or value == 'null' or pd.isna(value):  # 빈 문자열, 'null', NaN을 NULL로 처리
        return 'NULL'
    return value

# 'Outer Color', 'Top Color', 'Bottom Color' 컬럼을 변환
df['Outer Color'] = df['Outer Color'].apply(translate_color)
df['Top Color'] = df['Top Color'].apply(translate_color)
df['Bottom Color'] = df['Bottom Color'].apply(translate_color)

# 빈 문자열과 'null' 값 처리
df['Outerwear'] = df['Outerwear'].apply(convert_empty_to_null)
df['Top'] = df['Top'].apply(convert_empty_to_null)
df['Bottom'] = df['Bottom'].apply(convert_empty_to_null)
df['Outer Color'] = df['Outer Color'].apply(convert_empty_to_null)
df['Top Color'] = df['Top Color'].apply(convert_empty_to_null)
df['Bottom Color'] = df['Bottom Color'].apply(convert_empty_to_null)

# 변환된 데이터를 새로운 CSV 파일로 저장
df.to_csv(csv_file_path, index=False, encoding='utf-8-sig')

print(f"변환된 CSV 파일이 '{csv_file_path}'로 저장되었습니다.")



# CSV 파일 읽기 함수
def read_csv_file(file_path):
    recommendation_sets = []

    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        # 헤더 읽기
        next(reader)
        # 데이터 읽기
        for row in reader:
            recommendation_sets.append(row)

    return recommendation_sets

# 저장된 CSV 파일 읽기
recommendation_sets = read_csv_file(csv_file_path)

# 리스트로 저장 
# [0]=Top
set_1, set_2, set_3 = recommendation_sets
print("추천 1:", set_1)
print("추천 2:", set_2)
print("추천 3:", set_3)


# 웹 드라이버 설정
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # 화면을 표시하지 않음 (웹 드라이버가 브라우저를 띄우지 않고 백그라운드에서 실행)
options.add_argument('--no-sandbox')  # 보안 관련 문제를 피하기 위해 --no-sandbox 옵션 추가 (리눅스에서 필요)
# options.add_argument('--disable-dev-shm-usage')  # 자원 부족 문제를 피하기 위해 추가할 수 있는 옵션
driver = webdriver.Chrome(options=options)  # 설정된 옵션을 사용하여 Chrome 드라이버 인스턴스 생성


# 무신사 남성 인기 랭킹 페이지로 이동
url = 'https://www.musinsa.com/main/musinsa/recommend?gf=M'  # 무신사 남성 인기 랭킹 페이지 URL
driver.get(url)  # 웹 드라이버로 해당 URL로 이동

time.sleep(3)  # 페이지 로딩 대기 (페이지가 완전히 로드될 때까지 3초 대기)


try:
    # 팝업 배너 광고 닫기 버튼 클릭
    driver.find_element(By.XPATH, '/html/body/section/div[2]/button').click()
except (NoSuchElementException, ElementNotInteractableException):
    # 버튼이 없거나 상호작용이 불가능한 경우 예외 처리
    print("팝업 배너 광고 닫기 버튼을 찾을 수 없거나 클릭할 수 없습니다.")



# 전체->남성으로 변경 버튼 클릭
driver.find_element(By.XPATH, '//*[@id="commonLayoutFab"]/div/div/div/button[1]').click()
driver.find_element(By.XPATH, '//*[@id="commonLayoutFab"]/div/div/div/button[2]').click()
time.sleep(3)

# 첫 번째 검색창 이동
driver.find_element(By.XPATH, '//*[@id="commonLayoutHeader"]/section/div[2]/div/button[1]').click()


# 검색창을 찾아 검색어 입력 및 다음 작업 수행


def click_div_by_text(driver, div_text, wait_time=10):
    """
    주어진 텍스트가 포함된 div를 찾아 클릭하는 함수
    :param driver: Selenium WebDriver 객체
    :param div_text: 클릭할 div의 텍스트
    :param wait_time: div가 나타날 때까지 기다리는 시간 (초)
    """
    try:
        element = WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.XPATH, f"//div[contains(@class, 'gtm-click-button') and text()='{div_text}']"))
        )
        element.click()
        print(f"'{div_text}' 클릭 완료")
    except Exception as e:
        print(f"div '{div_text}' 클릭 실패: {e}")

def click_button_by_text(driver, button_text, wait_time=10):
    """
    주어진 텍스트가 포함된 버튼을 찾아 클릭하는 함수
    :param driver: Selenium WebDriver 객체
    :param button_text: 클릭할 버튼의 텍스트
    :param wait_time: 버튼이 나타날 때까지 기다리는 시간 (초)
    """
    try:
        element = WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.XPATH, f"//button[contains(@class, 'nGggL')]//p[text()='{button_text}']"))
        )
        element.click()
        print(f"'{button_text}' 버튼 클릭 완료")
    except Exception as e:
        print(f"버튼 '{button_text}' 클릭 실패: {e}")

def click_span_by_text(driver, span_text, wait_time=10):
    """
    주어진 텍스트가 포함된 span을 찾아 클릭하는 함수
    :param driver: Selenium WebDriver 객체
    :param span_text: 클릭할 span의 텍스트
    :param wait_time: span이 나타날 때까지 기다리는 시간 (초)
    """
    try:
        element = WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.XPATH, f"//span[text()='{span_text}']"))
        )
        element.click()
        print(f"'{span_text}' 클릭 완료")
    except Exception as e:
        print(f"'{span_text}' 클릭 실패: {e}")

def click_li_by_text(driver, span_text, wait_time=10):
    """
    주어진 텍스트가 포함된 span을 찾아 클릭하는 함수
    :param driver: Selenium WebDriver 객체
    :param span_text: 클릭할 span의 텍스트
    :param wait_time: span이 나타날 때까지 기다리는 시간 (초)
    """
    try:
        element = WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.XPATH, f"//label[text()='{span_text}']"))
        )
        element.click()
        print(f"'{span_text}' 클릭 완료")
    except Exception as e:
        print(f"'{span_text}' 클릭 실패: {e}")

def click_size_by_text(driver, span_text, wait_time=10):
    """
    주어진 텍스트가 포함된 span을 찾아 클릭하는 함수
    :param driver: Selenium WebDriver 객체
    :param span_text: 클릭할 span의 텍스트
    :param wait_time: span이 나타날 때까지 기다리는 시간 (초)
    """
    try:
        element = WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.XPATH, f"//button[text()='{span_text}']"))
        )
        element.click()
        print(f"'{span_text}' 클릭 완료")
    except Exception as e:
        print(f"'{span_text}' 클릭 실패: {e}")

def refresh_page(driver, delay=5):
    """
    Selenium을 사용하여 페이지를 새로고침하는 함수.

    Parameters:
        driver (webdriver): Selenium WebDriver 객체
        delay (int): 새로고침 후 대기 시간 (초)

    Usage:
        driver = webdriver.Chrome()
        driver.get('https://example.com')
        refresh_page(driver)
    """
    driver.refresh()  # 페이지 새로고침
    time.sleep(delay)  # 지정된 시간만큼 대기 (선택사항)

def handle_search_and_filter(driver, set_number_color, set_nubmer_size):
    try:
        # "컬러" 텍스트가 있는 div 클릭
        click_div_by_text(driver, "컬러")
        
        # 잠시 대기
        time.sleep(0.5)
        
        # "블랙" 텍스트가 있는 버튼 클릭         !!!!!!!!!!! 여기 동적으로 변수값 지정 !!!!!!!!!!!!!!! ,set_color 함수 변수값 
        click_button_by_text(driver, f'{set_number_color}')
        
        # 잠시 대기
        time.sleep(0.5)

        # "컬러" 텍스트가 있는 div 클릭
        click_size_by_text(driver, "사이즈")
        
        # 잠시 대기
        time.sleep(0.5)
        
        # "사이즈" 텍스트가 있는 버튼 클릭         !!!!!!!!!!! 여기 동적으로 변수값 지정 !!!!!!!!!!!!!!! ,set_size 함수 변수값 
        click_li_by_text(driver, set_nubmer_size if set_nubmer_size in ['S', 'M', 'L', 'XL'] else '2XL 이상')
        
        refresh_page(driver)

        # "무신사 추천순" 텍스트가 있는 span 클릭
        click_span_by_text(driver, "무신사 추천순")
        
        # "후기순" 텍스트가 있는 span 클릭
        click_span_by_text(driver, "후기순")
        
    except Exception as e:
        print(f"작업 중 오류 발생: {e}")


# 페이지 소스 가져오기
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')


# 이미지 다운로드 함수
def download_image(image_url, folder):
    try:
        # URL에서 쿼리 문자열 제거
        parsed_url = urlparse(image_url)
        image_name = os.path.basename(parsed_url.path)  # 파일 이름만 추출
        image_name = image_name.split('?')[0]  # 쿼리 문자열 제거
        
        # 유효하지 않은 파일 이름 문자 제거 (예: Windows에서 금지된 문자들)
        invalid_chars = ['?', ':', '*', '"', '<', '>', '|', '\\', '/', '#']
        for char in invalid_chars:
            image_name = image_name.replace(char, '_')
        
        # 파일명에 .png 확장자 붙이기
        image_name = image_name.split('_')[0] + '.png'  # 파일명에서 _ 이전 부분만 추출 후 .png 추가
        
        image_path = os.path.join(folder, image_name)
        
        # 이미지를 다운로드하여 지정된 폴더에 저장
        img_data = requests.get(image_url).content
        with open(image_path, 'wb') as file:
            file.write(img_data)
        print(f"이미지 {image_name}이 저장되었습니다.")
        return image_name  # 이미지 이름 반환
    except Exception as e:
        print(f"이미지 다운로드 오류: {e}")
        return None

# XPath에 맞는 텍스트와 이미지 URL을 추출하는 함수
def extract_text_and_image(driver, text_xpath, image_xpath):
    try:
        # 텍스트 추출
        text_element = driver.find_element(By.XPATH, text_xpath)
        text = text_element.text

        # 이미지 URL 추출
        img_element = driver.find_element(By.XPATH, image_xpath)  # 이미지 XPath 사용
        img_url = img_element.get_attribute("src") if img_element else None
        
        return text, img_url
    except Exception as e:
        print(f"Error: {e}")
        return None, None

# XPath를 동적으로 생성하는 함수 (텍스트용)
def generate_text_xpath(k, i, j):
    """
    i 값에 따라 동적으로 XPath를 생성하는 함수 (텍스트용).
    :param i: 요소의 인덱스
    :param j: j 값이 변경될 때마다 i는 다시 1부터 시작합니다.
    :return: 동적으로 생성된 XPath
    """
    xpath = f'//*[@id="commonLayoutContents"]/div/div[{k}]/div/div/div/div[{j}]/div/div[{i}]/div/div[2]/div/div[1]'
    return xpath

# XPath를 동적으로 생성하는 함수 (이미지용)
def generate_image_xpath(k, i, j):
    """
    i 값에 따라 동적으로 XPath를 생성하는 함수 (이미지용).
    :param i: 요소의 인덱스
    :param j: j 값이 변경될 때마다 i는 다시 1부터 시작합니다.
    :return: 동적으로 생성된 XPath
    """
    
    xpath = f'//*[@id="commonLayoutContents"]/div/div[{k}]/div/div/div/div[{j}]/div/div[{i}]/div/div[1]/div/a/div/img'
    return xpath


# 검색창을 찾아 검색어 입력
search_box_bottom = driver.find_element(By.XPATH, '//*[@id="commonSearchHome"]/main/header/div/input')

search_box_bottom.send_keys(f'{set_1[1]}')  # 검색어 동적 입력
search_box_bottom.send_keys(Keys.RETURN)  # 엔터 키를 눌러 검색 실행
# 함수를 호출하는 부분    handle_search_and_filter(driver, set_number_color, set_nubmer_size): 사전 세팅
handle_search_and_filter(driver, set_1[6], set_1[4])
# 이미지 저장 경로
image_folder = "downloaded_images/top"
os.makedirs(image_folder, exist_ok=True)

# 최종 데이터를 저장할 리스트
data_list = []

# Tag_name 초기화
tag_name_counter = 1

# 이미지 다운로드 함수
def download_image(img_url, save_folder):
    try:
        # 이미지 파일명 추출 (고유 ID 부분)
        file_name = img_url.split('/')[-1].split('_')[0] + ".jpg"
        response = requests.get(img_url, stream=True, timeout=10)
        if response.status_code == 200:
            file_path = os.path.join(save_folder, file_name)
            with open(file_path, 'wb') as img_file:
                for chunk in response.iter_content(1024):
                    img_file.write(chunk)
            return file_name  # 저장된 파일명 반환
        else:
            print(f"이미지 다운로드 실패: {img_url} (상태 코드: {response.status_code})")
            return None
    except Exception as e:
        print(f"이미지 다운로드 중 오류 발생: {e}")
        return None

# j 값과 i 값에 대한 반복
for k in range(1, 5):  # k 값 범위
    for j in range(1, 4):  # j 값 범위
        for i in range(1, 4):  # i 값 범위
            # 텍스트 및 링크 XPath 생성
            text_xpath = f'//*[@id="commonLayoutContents"]/div/div[{k}]/div/div/div/div[{j}]/div/div[{i}]/div/div[2]/div/div[1]'
            link_xpath = f'//*[@id="commonLayoutContents"]/div/div[{k}]/div/div/div/div[{j}]/div/div[{i}]/div/div[1]/div/a'
            image_xpath = f'//*[@id="commonLayoutContents"]/div/div[{k}]/div/div/div/div[{j}]/div/div[{i}]/div/div[1]/div/a/div/img'
            
            try:
                # 텍스트 추출
                text_element = driver.find_element(By.XPATH, text_xpath)
                text = text_element.text.split('\n')
                if len(text) >= 4:
                    brand = text[0]
                    name = text[1]
                    discount = text[2]
                    price = text[3]
                else:
                    continue

                # 링크 추출
                try:
                    link_element = driver.find_element(By.XPATH, link_xpath)
                    link = link_element.get_attribute('href')
                    last_part = link.split('/')[-1]  # 링크 마지막 부분 추출
                except Exception as link_error:
                    print(f"링크 XPath {link_xpath}에서 오류 발생: {link_error}")
                    last_part = ""

                # 이미지 URL 추출 및 다운로드
                try:
                    image_element = driver.find_element(By.XPATH, image_xpath)
                    img_url = image_element.get_attribute('src')
                    if img_url:
                        # 이미지 URL이 절대 경로가 아니라면 절대 경로로 변환
                        img_url = urljoin(driver.current_url, img_url)
                        downloaded_image_name = download_image(img_url, image_folder)
                    else:
                        downloaded_image_name = None
                except Exception as img_error:
                    print(f"이미지 XPath {image_xpath}에서 오류 발생: {img_error}")
                    downloaded_image_name = None

                # 데이터 추가
                data_list.append([brand, name, discount, price, last_part, tag_name_counter, 1])
                
                # Tag_name 증가
                tag_name_counter += 1

            except Exception as e:
                print(f"XPath {text_xpath}에서 오류 발생: {e}")

# 데이터 CSV로 저장
output_filename = 'extracted_product_data_top.csv'
with open(output_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['브랜드', '상품명', '할인율', '가격', '링크번호', 'Tag_name', 'Tag'])  # 헤더
    writer.writerows(data_list)  # 데이터 저장

print(f"모든 데이터가 {output_filename} 파일에 저장되었습니다.")

# 검색창을 찾아 검색어 입력 
driver.find_element(By.XPATH, '//*[@id="commonLayoutHeader"]/div/button[1]').click()
driver.find_element(By.XPATH, '//*[@id="commonSearchHome"]/main/header/div/button[1]').click()
search_box_bottom = driver.find_element(By.XPATH, '//*[@id="commonSearchHome"]/main/header/div/input')

search_box_bottom.send_keys(f'{set_1[2]}')  # 검색어 동적 입력
search_box_bottom.send_keys(Keys.RETURN)  # 엔터 키를 눌러 검색 실행
# 함수를 호출하는 부분    handle_search_and_filter(driver, set_number_color, set_nubmer_size):
handle_search_and_filter(driver, set_1[7], set_1[4])

# 이미지 저장 경로
image_folder = "downloaded_images/bottom"
os.makedirs(image_folder, exist_ok=True)

# 최종 데이터를 저장할 리스트
data_list = []

# Tag_name 초기화
tag_name_counter = 1

# 이미지 다운로드 함수
def download_image(img_url, save_folder):
    try:
        # 이미지 파일명 추출 (고유 ID 부분)
        file_name = img_url.split('/')[-1].split('_')[0] + ".jpg"
        response = requests.get(img_url, stream=True, timeout=10)
        if response.status_code == 200:
            file_path = os.path.join(save_folder, file_name)
            with open(file_path, 'wb') as img_file:
                for chunk in response.iter_content(1024):
                    img_file.write(chunk)
            return file_name  # 저장된 파일명 반환
        else:
            print(f"이미지 다운로드 실패: {img_url} (상태 코드: {response.status_code})")
            return None
    except Exception as e:
        print(f"이미지 다운로드 중 오류 발생: {e}")
        return None

# j 값과 i 값에 대한 반복
for k in range(1, 5):  # k 값 범위
    for j in range(1, 4):  # j 값 범위
        for i in range(1, 4):  # i 값 범위
            # 텍스트 및 링크 XPath 생성
            text_xpath = f'//*[@id="commonLayoutContents"]/div/div[{k}]/div/div/div/div[{j}]/div/div[{i}]/div/div[2]/div/div[1]'
            link_xpath = f'//*[@id="commonLayoutContents"]/div/div[{k}]/div/div/div/div[{j}]/div/div[{i}]/div/div[1]/div/a'
            image_xpath = f'//*[@id="commonLayoutContents"]/div/div[{k}]/div/div/div/div[{j}]/div/div[{i}]/div/div[1]/div/a/div/img'
            
            try:
                # 텍스트 추출
                text_element = driver.find_element(By.XPATH, text_xpath)
                text = text_element.text.split('\n')
                if len(text) >= 4:
                    brand = text[0]
                    name = text[1]
                    discount = text[2]
                    price = text[3]
                else:
                    continue

                # 링크 추출
                try:
                    link_element = driver.find_element(By.XPATH, link_xpath)
                    link = link_element.get_attribute('href')
                    last_part = link.split('/')[-1]  # 링크 마지막 부분 추출
                except Exception as link_error:
                    print(f"링크 XPath {link_xpath}에서 오류 발생: {link_error}")
                    last_part = ""

                # 이미지 URL 추출 및 다운로드
                try:
                    image_element = driver.find_element(By.XPATH, image_xpath)
                    img_url = image_element.get_attribute('src')
                    if img_url:
                        # 이미지 URL이 절대 경로가 아니라면 절대 경로로 변환
                        img_url = urljoin(driver.current_url, img_url)
                        downloaded_image_name = download_image(img_url, image_folder)
                    else:
                        downloaded_image_name = None
                except Exception as img_error:
                    print(f"이미지 XPath {image_xpath}에서 오류 발생: {img_error}")
                    downloaded_image_name = None

                # 데이터 추가
                data_list.append([brand, name, discount, price, last_part, tag_name_counter, 1])
                
                # Tag_name 증가
                tag_name_counter += 1

            except Exception as e:
                print(f"XPath {text_xpath}에서 오류 발생: {e}")

# 데이터 CSV로 저장
output_filename = 'extracted_product_data_bottom.csv'
with open(output_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['브랜드', '상품명', '할인율', '가격', '링크번호', 'Tag_name', 'Tag'])  # 헤더
    writer.writerows(data_list)  # 데이터 저장

print(f"모든 데이터가 {output_filename} 파일에 저장되었습니다.")

# 검색창을 찾아 검색어 입력 
driver.find_element(By.XPATH, '//*[@id="commonLayoutHeader"]/div/button[1]').click()
driver.find_element(By.XPATH, '//*[@id="commonSearchHome"]/main/header/div/button[1]').click()
search_box_bottom = driver.find_element(By.XPATH, '//*[@id="commonSearchHome"]/main/header/div/input')

search_box_bottom.send_keys(f'{set_1[0]}')  # 검색어 동적 입력
search_box_bottom.send_keys(Keys.RETURN)  # 엔터 키를 눌러 검색 실행
# 이미지 저장 경로
image_folder = "downloaded_images/outer"
os.makedirs(image_folder, exist_ok=True)

# 최종 데이터를 저장할 리스트
data_list = []

# Tag_name 초기화
tag_name_counter = 1

# 이미지 다운로드 함수
def download_image(img_url, save_folder):
    try:
        # 이미지 파일명 추출 (고유 ID 부분)
        file_name = img_url.split('/')[-1].split('_')[0] + ".jpg"
        response = requests.get(img_url, stream=True, timeout=10)
        if response.status_code == 200:
            file_path = os.path.join(save_folder, file_name)
            with open(file_path, 'wb') as img_file:
                for chunk in response.iter_content(1024):
                    img_file.write(chunk)
            return file_name  # 저장된 파일명 반환
        else:
            print(f"이미지 다운로드 실패: {img_url} (상태 코드: {response.status_code})")
            return None
    except Exception as e:
        print(f"이미지 다운로드 중 오류 발생: {e}")
        return None

# j 값과 i 값에 대한 반복
for k in range(1, 5):  # k 값 범위
    for j in range(1, 4):  # j 값 범위
        for i in range(1, 4):  # i 값 범위
            # 텍스트 및 링크 XPath 생성
            text_xpath = f'//*[@id="commonLayoutContents"]/div/div[{k}]/div/div/div/div[{j}]/div/div[{i}]/div/div[2]/div/div[1]'
            link_xpath = f'//*[@id="commonLayoutContents"]/div/div[{k}]/div/div/div/div[{j}]/div/div[{i}]/div/div[1]/div/a'
            image_xpath = f'//*[@id="commonLayoutContents"]/div/div[{k}]/div/div/div/div[{j}]/div/div[{i}]/div/div[1]/div/a/div/img'
            
            try:
                # 텍스트 추출
                text_element = driver.find_element(By.XPATH, text_xpath)
                text = text_element.text.split('\n')
                if len(text) >= 4:
                    brand = text[0]
                    name = text[1]
                    discount = text[2]
                    price = text[3]
                else:
                    continue

                # 링크 추출
                try:
                    link_element = driver.find_element(By.XPATH, link_xpath)
                    link = link_element.get_attribute('href')
                    last_part = link.split('/')[-1]  # 링크 마지막 부분 추출
                except Exception as link_error:
                    print(f"링크 XPath {link_xpath}에서 오류 발생: {link_error}")
                    last_part = ""

                # 이미지 URL 추출 및 다운로드
                try:
                    image_element = driver.find_element(By.XPATH, image_xpath)
                    img_url = image_element.get_attribute('src')
                    if img_url:
                        # 이미지 URL이 절대 경로가 아니라면 절대 경로로 변환
                        img_url = urljoin(driver.current_url, img_url)
                        downloaded_image_name = download_image(img_url, image_folder)
                    else:
                        downloaded_image_name = None
                except Exception as img_error:
                    print(f"이미지 XPath {image_xpath}에서 오류 발생: {img_error}")
                    downloaded_image_name = None

                # 데이터 추가
                data_list.append([brand, name, discount, price, last_part, tag_name_counter, 1])
                
                # Tag_name 증가
                tag_name_counter += 1

            except Exception as e:
                print(f"XPath {text_xpath}에서 오류 발생: {e}")

# 데이터 CSV로 저장
output_filename = 'extracted_product_data_outer.csv'
with open(output_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['브랜드', '상품명', '할인율', '가격', '링크번호', 'Tag_name', 'Tag'])  # 헤더
    time.sleep(1)
    writer.writerows(data_list)  # 데이터 저장

print(f"모든 데이터가 {output_filename} 파일에 저장되었습니다.")









def merge_files_sequentially(top_file, bottom_file, outer_file, output_file):
    # 각 CSV 파일을 동적으로 읽기
    top_df = pd.read_csv(top_file)
    bottom_df = pd.read_csv(bottom_file)
    outer_df = pd.read_csv(outer_file)

    # 각 파일에서 첫 번째 행을 차례대로 결합
    combined_data = []
    
    # 각 파일에서 데이터를 차례대로 반복해서 결합
    for i in range(min(len(top_df), len(bottom_df), len(outer_df))):  # 세 파일 모두 길이가 같다고 가정
        combined_data.append(top_df.iloc[i])    # Top에서 i번째 행 추가
        combined_data.append(bottom_df.iloc[i]) # Bottom에서 i번째 행 추가
        combined_data.append(outer_df.iloc[i])  # Outer에서 i번째 행 추가

    # 새로운 DataFrame 생성 (결합된 데이터)
    combined_df = pd.DataFrame(combined_data)

    # 결과를 새로운 CSV로 저장
    combined_df.to_csv(output_file, index=False)
    print(f"{output_file} 파일이 성공적으로 생성되었습니다!")

# 동적으로 파일명을 받아와서 처리
merge_files_sequentially('extracted_product_data_top.csv', 
                        'extracted_product_data_bottom.csv', 
                        'extracted_product_data_outer.csv', 
                        'combined_product_data.csv')

def split_csv_and_update_tags(input_file, output_prefix, rows_per_file=3, max_files=3):
    # CSV 파일 읽기
    df = pd.read_csv(input_file)
    
    # 데이터의 총 행 수
    total_rows = len(df)
    
    # 최대 3개의 파일만 생성하도록 제한
    file_count = 0
    
    # 3줄씩 나누어 파일로 저장
    for start_row in range(0, total_rows, rows_per_file):
        if file_count >= max_files:  # 최대 파일 수만큼 저장 후 종료
            break
        
        # 부분 DataFrame 생성 (3줄씩)
        end_row = min(start_row + rows_per_file, total_rows)
        df_chunk = df.iloc[start_row:end_row].copy()  # 복사본 생성 (원본 수정 방지)
        
        # Tag 값을 1, 2, 3으로 순차적으로 설정
        df_chunk['Tag'] = range(1, len(df_chunk) + 1)
        
        # 새로운 파일 이름 생성
        output_file = f"{output_prefix}{file_count+1}.csv"
        
        # 부분 DataFrame을 새로운 CSV 파일로 저장
        df_chunk.to_csv(output_file, index=False)
        print(f"파일 '{output_file}' 이(가) 성공적으로 생성되었습니다!")
        
        # 파일 카운트 증가
        file_count += 1

# 사용 예시
input_file = 'combined_product_data.csv'  # 실제 파일 경로로 변경
output_prefix = 'recommend'    # 출력 파일의 접두어
split_csv_and_update_tags(input_file, output_prefix)

# 경로 설정
image_folders = {
    1: "downloaded_images/top",
    2: "downloaded_images/bottom",
    3: "downloaded_images/outer",
}
output_folder = "recommend_images_output"

# 출력 폴더가 없으면 생성
os.makedirs(output_folder, exist_ok=True)

# CSV 파일 리스트
csv_files = ["recommend1.csv", "recommend2.csv", "recommend3.csv"]

# 접두사 설정
tag_prefix = {
    1: "rec",
    2: "reco",
    3: "recom"
}

def find_file_in_folders(link_number, folders):
    """
    여러 폴더를 탐색하여 파일을 찾는 함수.

    Parameters:
        link_number (str): 찾으려는 파일의 링크 번호
        folders (dict): 탐색할 폴더의 딕셔너리 {tag: folder_path}

    Returns:
        str: 파일 경로 (찾았을 경우), None (찾지 못했을 경우)
    """
    for folder in folders.values():
        file_path = os.path.join(folder, f"{link_number}.jpg")
        if os.path.exists(file_path):
            return file_path
    return None

# 각 CSV 파일 처리
for csv_file in csv_files:
    # CSV 파일 읽기
    df = pd.read_csv(csv_file)

    # CSV 파일의 각 행 처리
    for index, row in df.iterrows():
        link_number = row['링크번호']  # 링크 번호 가져오기
        tag_name = row['Tag_name']  # Tag_name 가져오기

        # 이미지 파일 경로 찾기
        src_file = find_file_in_folders(link_number, image_folders)

        if src_file:
            # 새로운 파일 이름 생성
            prefix = tag_prefix.get(tag_name, "unknown")
            new_file_name = f"{prefix}{index+1}.png"
            new_file_path = os.path.join(output_folder, new_file_name)

            # 파일 복사
            shutil.copy(src_file, new_file_path)
            print(f"'{src_file}' 파일을 '{new_file_path}'로 복사했습니다.")
            time.sleep(0.5)
        else:
            print(f"링크번호 {link_number}에 해당하는 파일을 찾을 수 없습니다.")

# 처리 완료 메시지
print("이미지 파일들이 성공적으로 복사되고 저장되었습니다.")

def remove_files_and_folders(file_list, folder_list):
    """
    주어진 CSV 파일 목록과 폴더 목록에서 각 파일 및 폴더를 삭제합니다.

    Args:
        file_list (list): 삭제할 CSV 파일들의 경로 리스트.
        folder_list (list): 삭제할 폴더들의 경로 리스트.
    """
    try:
        # 파일 삭제
        for file in file_list:
            if os.path.exists(file):
                os.remove(file)  # 파일 삭제
                print(f"파일 '{file}' 이(가) 성공적으로 삭제되었습니다.")
            else:
                print(f"파일 '{file}' 이(가) 존재하지 않습니다.")
        
        # 폴더 삭제
        for folder in folder_list:
            if os.path.exists(folder):
                shutil.rmtree(folder)  # 폴더와 그 안의 모든 파일 삭제
                print(f"폴더 '{folder}' 이(가) 성공적으로 삭제되었습니다.")
            else:
                print(f"폴더 '{folder}' 이(가) 존재하지 않습니다.")
                
    except Exception as e:
        print(f"오류 발생: {e}")

# 삭제할 CSV 파일 목록
csv_files_to_remove = [
    'extracted_product_data_bottom.csv', 
    'extracted_product_data_outer.csv', 
    'extracted_product_data_top.csv',
    'combined_product_data.csv',
    
]

# 삭제할 폴더 목록
folders_to_remove = [
    'downloaded_images'
]

# 파일 및 폴더 삭제 실행
remove_files_and_folders(csv_files_to_remove, folders_to_remove)

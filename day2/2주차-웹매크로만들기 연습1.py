# import 할 것들은 항상 같으니 그대로 복사해서 쓰시면 됩니다.
#------여기서부터 복사해서 쓰는 내용 시작----------------------------------------
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

#크롬 드라이버 자동 업데이트용
from webdriver_manager.chrome import ChromeDriverManager

#사람이라고 생각되도록 장치를 위함
import time
import pyautogui
import pyperclip

#브라우저 꺼짐 방지 옵션 설정
크롬옵션객체 = Options()
크롬옵션객체.add_experimental_option("detach", True)

#크롬 드라이버 자동 업데이트 설치 하고 서비스객체에 넣음
서비스객체 = Service(executable_path=ChromeDriverManager().install())
드라이버 = webdriver.Chrome(service=서비스객체, options=크롬옵션객체)

#드라이버에 설정 적용
드라이버.implicitly_wait(5)  #웹페이지 다 뜰때까지 5초는 기다린다.
드라이버.maximize_window()   #화면최대화

#------여기까지 복사해서 쓰기---------------------------------------------------------

#여기서부터 웹 매크로 코딩 시작

드라이버.get('https://www.naver.com')

#검색입력 객체잡기
검색입력 = 드라이버.find_element(By.XPATH, '//*[@id="query"]')
검색입력.click()

#검색어 입력
pyperclip.copy('덕이중학교 급식')
pyautogui.hotkey('ctrl','v')

검색버튼 = 드라이버.find_element(By.XPATH, '//*[@id="sform"]/fieldset/button')

#검색버튼 객체잡기
검색버튼 = 드라이버.find_element(By.XPATH, '//*[@id="sform"]/fieldset/button')
검색버튼.click()
time.sleep(2)

날짜요소다가져와 = 드라이버.find_elements(By.CLASS_NAME, 'cm_date')

파이썬리스트=[]
for 찾아온거 in 날짜요소다가져와:
    if 찾아온거.text != '':
        파이썬리스트.append(찾아온거.text)
a = 파이썬리스트
급식요소다가져와1 = 드라이버.find_elements(By.CLASS_NAME, 'text')
파이썬리스트1=[]
for 찾아온거1 in 급식요소다가져와1:
    if 찾아온거1.text != ' ':
        파이썬리스트1.append(찾아온거1.text)
b = 파이썬리스트1

c = [a,b]

print (c)

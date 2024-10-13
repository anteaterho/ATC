#모듈 불러오기
import io
import requests
import pandas as pd
import tkinter as tk
import tkinter.font

#기본 API 접속하는 url
domain = "https://apihub.kma.go.kr/api/typ01/url/kma_sfctm2.php?"

#요청인자 1 - 관측 시간
tm = "202410100800&"

#요청인자 2 - 지점 번호 (0이면 전국입니다.) https://data.kma.go.kr/tmeta/stn/selectStnList.do <-여기에서 찾을 수 있어요
stn = "stn=99&"

#요청인자 3 - 도움말 추가 (0으로 해서 지워야 데이터를 잘 받아 옵니다.)
help = "help=0&"

#요청인자 4 - 인증키 (자신의 API키를 입력해야 합니다.)
auth = "authKey=bkOXVufWQtqDl1bn1vLalA"

#url 완성하기
url = domain + tm + stn + help + auth

#지상관측 데이터 확인, get 요청
response = requests.get(url) 

#데이터 공백으로 파싱해서 저장
data = pd.read_csv(io.StringIO(response.text), sep='\s+', skiprows=2)

#데이터 프레임을 csv 파일로 저장
data.to_csv('./api로불러온데이터2.csv', index=False)

#데이터 확인
#print(data)

#데이터 정보 확인
#print(data.info())

#TA 열만 빼서 dataTA 데이터 프레임 만들기
dataTA = data[['TA']]

#TA 데이터 확인
#print(dataTA)

#dataTA 프레임에서 1번째 행의 TA열 값을 가져와서 '현재기온'에 넣기
현재기온 = dataTA.iloc[1]['TA']


#현재기온 확인하기
#print(현재기온)




'''
여기서부터는 GUI 구성
'''

window = tk.Tk()

#창 제목 설정
window.title('weather')

#창 크기 설정하기 (창 크기는 변경 가능)
window.geometry('500x400+100+100')

#배경 색상 설정하기
window.configure(bg='pink')
#참고) 원하는 색상값을 넣을 수도 있다.
#window.configure(bg='#6ba4ff')

#글씨 크기 설정
font=tk.font.Font(size=30)

tk_label = tk.Label(window, text='현재도시 : 파주', width=50, font=font, bg='pink')
tk_label.pack(side='top', expand=False, ipady=30, anchor='center')

tk_label = tk.Label(window, text='현재기온 : '+현재기온, width=50, font=font, bg='white')
tk_label.pack(side='top', expand=False, fill='x', ipady=30, anchor='center')
#tk_label = tk.Label(window, text='현재풍향 : '+현재풍향, width=50, font=font, bg='cyan2')
tk_label.pack(side='top', expand=False, fill='x', ipady=30, anchor='center')


window.mainloop()
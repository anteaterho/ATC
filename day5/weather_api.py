import io
import requests
import pandas as pd
import tkinter as tk
import tkinter.font

domain = "https://apihub.kma.go.kr/api/typ01/url/kma_sfctm2.php?"   ##기본 API url
tm = "202410100800&"                                                ## 관측 시간
stn = "stn=99&"                                                     ## 지점 번호
help = "help=0&"                                                    ## 도움말 제거
auth = "authKey=bkOXVufWQtqDl1bn1vLalA"                              ## 인증키
url = domain + tm + stn + help + auth

response = requests.get(url)

data = pd.read_csv(io.StringIO(response.text), sep='\s+', skiprows=2)

data.to_csv('./weather_status_api.csv', index=False)

print('data : ', data)
print('data info : ', data.info())

# 데이터 추출 부분 수정
dataTA = data[['TA']]
dataWD = data[['WD']]  # 풍향 데이터 추출
dataWS = data[['WS']]  # 풍속 데이터 추출

print('dataTA : ', dataTA)
print('dataWD : ', dataWD)
print('dataWS : ', dataWS)

temperature = dataTA.iloc[1]['TA']
wind_direction = dataWD.iloc[1]['WD']
wind_speed = dataWS.iloc[1]['WS']

'''
gui
'''

window = tk.Tk()

window.title('날씨')
window.geometry('500x500+100+100')  # 창 크기를 조금 늘렸습니다
window.configure(bg='pink')

font = tk.font.Font(size=25)  # 글꼴 크기를 조금 줄였습니다

tk_label = tk.Label(window, text='현재도시 : 파주', width=50, font=font, bg='pink')
tk_label.pack(side='top', expand=False, ipady=20, anchor='center')

tk_label = tk.Label(window, text='현재기온 : ' + str(temperature) + '°C', width=50, font=font, bg='white')
tk_label.pack(side='top', expand=False, fill='x', ipady=20, anchor='center')

tk_label = tk.Label(window, text='풍향 : ' + str(wind_direction) + '°', width=50, font=font, bg='lightblue')
tk_label.pack(side='top', expand=False, fill='x', ipady=20, anchor='center')

tk_label = tk.Label(window, text='풍속 : ' + str(wind_speed) + 'm/s', width=50, font=font, bg='lightgreen')
tk_label.pack(side='top', expand=False, fill='x', ipady=20, anchor='center')

window.mainloop()

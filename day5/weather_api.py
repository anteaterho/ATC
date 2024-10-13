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

dataTA = data[['TA']]

print('dataTA : ' , dataTA)

temperature = dataTA.iloc[1]['TA']

'''
gui
'''

window = tk.Tk()

window.title('weather')
window.geometry('500x400+100+100')
window.configure(bg='pink')

font = tk.font.Font(size=30)

tk_label = tk.Label(window, text='현재도시 : 파주', width=50, font=font, bg='pink')
tk_label.pack(side='top', expand=False, ipady=30, anchor='center')

tk_label = tk.Label(window, text='현재기온 : ' + temperature, width=50, font=font, bg='white')
tk_label.pack(side='top', expand=False, fill='x', ipady=30, anchor='center')

window.mainloop()
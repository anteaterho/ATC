import tkinter as tk
from tkinter import messagebox

# 윈도우 생성
window = tk.Tk()
window.geometry('500x300')  # 창 크기 설정
window.title('현수가 만든 프로그램')  # 창 제목 설정

# 라벨 생성 및 배치
label = tk.Label(window, text='이 프로그램은 나의 첫 프로그램이다', font=('Arial', 14))
label.pack(pady=10)  # 상단 여백을 추가하여 중앙 배치

# 버튼 클릭 이벤트 처리 함수
def on_click():
    messagebox.showinfo('1번 문제', '오리가 얼면?')
    messagebox.showinfo('1번 문제', '5')
    messagebox.showinfo('1번 문제', '4')
    messagebox.showinfo('1번 문제', '3')
    messagebox.showinfo('1번 문제', '2')
    messagebox.showinfo('1번 문제', '1')
    messagebox.showinfo('1번 문제', '언덕')
    messagebox.showinfo('ㅋ','ㅋㅋㅋ')
# '이걸 눌러봐' 버튼 생성 및 배치
button1 = tk.Button(window, text='이걸 눌러봐', command=on_click)
button1.pack(pady=20)  # 위쪽 여백을 추가하여 중앙 배치
# 프로그램 종료 함수
def quit_program():
    messagebox.showerror('확인', '프로그램을 종료하시겠습니까?')
    window.quit()

# '종료' 버튼 생성 및 배치
button2 = tk.Button(window, text='종료', command=quit_program)
button2.pack(pady=10)  # 위쪽 여백을 추가하여 중앙 배치

# 이벤트 루프 실행
window.mainloop()

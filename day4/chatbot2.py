import tkinter as tk
from tkinter import scrolledtext
from soynlp.tokenizer import RegexTokenizer
import random


tokenizer = RegexTokenizer()

responses = {
        "안녕하세요": "안녕하세요! 무엇을 도와드릴까요?",
        "이름이 뭐에요?": "저는 간단한 채팅봇입니다.",
        "날씨 어때요?": "저는 날씨를 알 수 없습니다. 직접 확인해보세요!",
        "종료": "대화가 종료되었습니다. 안녕히 가세요!",
        "김재원은 김치볶음밥을 좋아하나요?": "김치볶음밥을 너무 좋아합니다."
        }
game_active = False
secret_number = ""
attempts = 0

def preprocess_text(text):
    return tokenizer.tokenize(text)

def compute_similarity(text1, text2):
    tokens1 = set(preprocess_text(text1))
    tokens2 = set(preprocess_text(text2))
    return len(tokens1.intersection(tokens2)) / len(tokens1.union(tokens2))

def start_number_game():
    global game_active, secret_number, attempts
    game_active = True
    attempts = 0
    digits = random.sample(range(0,10), 3)
    secret_number = "".join(map(str, digits))
    return "지금부터 숫자 게임을 시작하지. 세 자리 숫자를 생각했어. 이제 내가 생각한 수가 무엇인지 맞춰봐."

def evaluate_guess(user_input):
    global attempts
    attempts += 1
    if len(user_input) !=3 or not user_input.isdigit():
        return "세 자리 숫자를 입력하세요."
    strike, ball, out = 0, 0, 0
    for i in range(3):
        if user_input[i] == secret_number[i]:
            strike += 1
        elif user_input[i] in secret_number:
            ball += 1
        else:
            out += 1
    if strike == 3:
        result = f"3 스트라이크! {attempts}번 만에 맞추셨습니다! 게임을 종료합니다."
        reset_game()
        return result
    else:
        return f"{strike} 스트라이크, {ball} 볼, {out} 아웃"
   
def reset_game():
    global game_active, secret_number, attempts
    game_active = False
    secret_number = ""
    attempts = 0

def chatbot_response(user_input):
    global game_active
    if game_active:
        return evaluate_guess(user_input)
    highest_similarity = 0
    best_response = "죄송합니다, 이해하지 못했습니다."
   
    if compute_similarity(user_input, "나랑 숫자게임하자") > 0.5:
        return start_number_game()
   
    for question, response in responses.items():
        similarity = compute_similarity(user_input, question)
        if similarity > highest_similarity:
            highest_similarity = similarity
            best_response = response    
        return best_response
   
def send_message():
    user_input = entry.get()
    if user_input:
        chat_area.config(state='normal')
        chat_area.insert(tk.END, "나: " + user_input + "\n")
        response = chatbot_response(user_input)
        chat_area.insert(tk.END, "봇: " + response + "\n")
        chat_area.config(state='disabled')
        entry.delete(0, tk.END)
        chat_area.yview(tk.END)

root = tk.Tk()
root.title("간단한 채팅봇")


chat_area = scrolledtext.ScrolledText(root, state='disabled', width=50, height=20)
chat_area.grid(row=0, column=0, columnspan=2)

entry= tk.Entry(root, width=40)
entry.grid(row=1, column=0)

send_button = tk.Button(root, text="전송", command=send_message)
send_button.grid(row=1, column=1)
                       
root.mainloop()
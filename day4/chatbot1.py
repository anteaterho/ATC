import tkinter as tk
from tkinter import scrolledtext
from soynlp.tokenizer import RegexTokenizer
import random

tokenizer = RegexTokenizer()

responses = {"hello": "hi, how can i help ?","what is your name?": "i am simple chatbot.","weather": "sorry, i dont know anything about weather", "exit": "exiting program, good bye!"}
game_active = False
secret_number = ""
attempts = 0
def preprocess_text(text):
        return tokenizer.tokenize(text)

def compute_similarity(text1, text2):
        tokens1 = set(preprocess_text(text1))
        tokens2 = set(preprocess_text(text2))
        return len(tokens1.intersection(tokens2))/ len(tokens1.union(tokens2))

def start_number_game():
        global game_active, secret_number, attempts
        game_active - True

        digits = random.sample(range(0,10),3)
        secret_number = "".join(map(str, digits))
        return 'game start, guess 3-digit number'

def evaluate_guess(user_input):
        global attempts
        attempts +=1
        if len(user_input) !=3 or not user_input.isdigit():
              return 'input 3 digit number'
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
        highest_similarity = 0
        best_response =  'sorry, i did not understand.'

        if compute_similarity(user_input, "나랑 숫자게임하자") > 0.5:
                return start_number_game()

        for question, responses in responses.itmes():
                similarity = compute_similarity(user_input,)
                if similarity > highest_similarity:
                        hightst_similarity = similarity
                        best_response = responses
                        return best_response


root = tk.Tk()
root.title('simple chatbot')
def send_message():
    user_input = entry.get()
    if user_input:
        chat_area.config(state = 'normal')
        chat_area.insert(tk.END, 'me:' + user_input + '\n')
        response = chatbot_response(user_input)
        chat_area.insert(tk.END, 'bot:' + response + '\n')
        chat_area.config(state = 'disabled')
        entry.delete(0, tk.END)
        chat_area.yview(tk.END)
chat_area = scrolledtext.ScrolledText(root, state = 'disabled',width = 50, height = 20)
chat_area.grid(row = 0, column = 0, columnspan = 2)

entry = tk.Entry(root, width = 40)
entry.grid(row = 1, column = 0)

send_button = tk.Button(root, text = 'send', command = send_message)
send_button.grid(row = 1, column = 1)




root.mainloop()

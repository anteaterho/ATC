def number_game():
    import random as r
    user_input = str(input())
    attempts = 0
    digits = r.sample(range(0,10), 3)
    secret_number = "".join(map(str, digits))
    def evaluate_guess(user_input):
        global attempts
        attempts += 1
        if len(user_input) !=3 or not user_input.isdigit():
            print( "세 자리 숫자를 입력하세요." )
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

            print(result)
        else:
            print( f"{strike} 스트라이크, {ball} 볼, {out} 아웃")

    
number_game()
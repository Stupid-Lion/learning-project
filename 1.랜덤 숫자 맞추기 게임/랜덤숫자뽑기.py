import random

r = random.randint(1,100)

# print(r)

game_count = 1
while True:
    try:
        my = int(input("1~100까지 입력하세요 :"))
        if my > r:
            print("다운")
        elif my < r:
            print("업")
        elif my == r:
            print(f"맞추셨습니다.{game_count}회 만에 맞추셨습니다.")
            break
        game_count = game_count + 1
    except Exception as e :
        print("에러발생:",e)
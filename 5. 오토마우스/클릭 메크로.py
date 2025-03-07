import pyautogui
import time
import pyperclip

input("반복클릭할 위치에 마우스를 두고 엔터를 입력해주세요")
poc = pyautogui.position()
print(f"반복클릭할 위치 :{poc}")
num = int(input("몇번 클릭하실 건가요?: "))
delay = float(input("클릭 사이지연시간(초): "))
print("3초후에 매크로가 실행됩니다.")
for e in range(3):
    print(e+1)
    time.sleep(1)

for i in range(num):
    pyautogui.click(poc)
    time.sleep(delay)
print("종료")
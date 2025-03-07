import pyautogui
import time
import pyperclip
in_text = input("검색어를 입력하세요:")
pyautogui.moveTo(1251,250,0.2)
pyautogui.click()
time.sleep(1)
pyperclip.copy(in_text)
pyautogui.hotkey("ctrl","v")
time.sleep(0.5)
pyautogui.write(["enter"])
time.sleep(1)

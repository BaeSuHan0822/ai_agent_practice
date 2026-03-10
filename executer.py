import pyautogui
import pyperclip
import time
### import schedule
import subprocess

subprocess.run(["osascript", "-e", 'tell application "KakaoTalk" to activate'])
time.sleep(3) # 창이 앞으로 올 때까지 3초 대기

pyautogui.hotkey("command","f")
time.sleep(1)

pyperclip.copy("python test")
pyautogui.hotkey("command","v")
time.sleep(1)

pyautogui.press("enter")
time.sleep(1)

pyperclip.copy("Hi")
pyautogui.hotkey("command","v")
time.sleep(1)

### pyautogui.press("enter")

print("{}에게 메시지 전송 완료!")
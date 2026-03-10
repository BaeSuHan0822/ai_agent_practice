import pyautogui
import pyperclip
import time
### import schedule
import subprocess
import sys

TARGET_NAME = "python test"
MESSAGE_TEXT = "Hi"


def is_kakaotalk_frontmost() -> bool:
    result = subprocess.run(
        [
            "osascript",
            "-e",
            'tell application "System Events" to get name of first process whose frontmost is true',
        ],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip() == "KakaoTalk"


def get_focused_ui_role_info() -> tuple[str, str]:
    script = """
tell application "System Events"
    tell process "KakaoTalk"
        set focusedElement to value of attribute "AXFocusedUIElement"
        set elementRole to role of focusedElement
        set elementSubrole to ""
        try
            set elementSubrole to subrole of focusedElement
        end try
        return elementRole & "|" & elementSubrole
    end tell
end tell
"""
    result = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True,
        text=True,
        check=True,
    )
    role_info = result.stdout.strip().split("|", 1)
    if len(role_info) == 1:
        return role_info[0], ""
    return role_info[0], role_info[1]


def wait_until_search_field_focused(timeout_sec: float = 3.0) -> bool:
    deadline = time.time() + timeout_sec
    last_role = ""
    last_subrole = ""
    while time.time() < deadline:
        try:
            role, subrole = get_focused_ui_role_info()
        except subprocess.CalledProcessError:
            time.sleep(0.2)
            continue
        last_role, last_subrole = role, subrole
        # Search field is usually AXTextField/AXSearchField.
        if role == "AXTextField" or subrole == "AXSearchField":
            return True
        time.sleep(0.2)
    if last_role or last_subrole:
        print(f"현재 포커스 요소: role={last_role}, subrole={last_subrole}")
    return False


def send_cmd_f_via_osascript() -> None:
    subprocess.run(
        [
            "osascript",
            "-e",
            'tell application "System Events" to keystroke "f" using command down',
        ],
        check=True,
    )


def focus_search_field() -> bool:
    # 1차: pyautogui 단축키
    pyautogui.hotkey("command", "f")
    if wait_until_search_field_focused():
        return True

    # 2차: AppleScript 단축키
    try:
        send_cmd_f_via_osascript()
    except subprocess.CalledProcessError:
        return False
    return wait_until_search_field_focused()


def get_focused_ui_value() -> str:
    script = """
tell application "System Events"
    tell process "KakaoTalk"
        set focusedElement to value of attribute "AXFocusedUIElement"
        set elementValue to ""
        try
            set elementValue to value of focusedElement as text
        end try
        return elementValue
    end tell
end tell
"""
    result = subprocess.run(
        ["osascript", "-e", script],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def open_chat_from_search(keyword: str) -> bool:
    # 1차: 검색 결과 첫 항목 선택 후 진입
    pyautogui.press("down")
    time.sleep(0.2)
    pyautogui.press("enter")
    time.sleep(1)
    if get_focused_ui_value() != keyword:
        return True

    # 2차: Enter 재시도
    pyautogui.press("enter")
    time.sleep(1)
    if get_focused_ui_value() != keyword:
        return True

    return False

subprocess.run(["osascript", "-e", 'tell application "KakaoTalk" to activate'])
time.sleep(3) # 창이 앞으로 올 때까지 3초 대기

if not is_kakaotalk_frontmost():
    print("포커스 확인 실패: 현재 전면 앱이 KakaoTalk이 아닙니다.")
    sys.exit(1)

print("포커스 확인 성공: KakaoTalk이 전면 앱입니다.")

if not focus_search_field():
    print("검색창 포커스 확인 실패: Cmd+F 후 검색 필드가 활성화되지 않았습니다.")
    print("macOS 손쉬운 사용/자동화 권한(터미널 또는 Python, System Events)을 확인하세요.")
    sys.exit(1)

print("검색창 포커스 확인 성공")

pyperclip.copy(TARGET_NAME)
pyautogui.hotkey("command","v")
time.sleep(1)

if not open_chat_from_search(TARGET_NAME):
    print("채팅방 진입 실패: 검색창에 머물러 있어 메시지 전송을 중단합니다.")
    sys.exit(1)

print("채팅방 진입 성공")

pyperclip.copy(MESSAGE_TEXT)
pyautogui.hotkey("command","v")
time.sleep(1)

pyautogui.press("enter")

print(f"{TARGET_NAME}에게 메시지 전송 완료!")

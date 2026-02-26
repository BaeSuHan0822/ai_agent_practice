# from my_own_agent.agent import main


# if __name__ == "__main__":
#     main()

import subprocess,os

def read_meet_code() :
    path = os.path.expanduser("~/Library/Mobile Documents/com~apple~CloudDocs/MeetBridge/latest_meet.txt")
    if os.path.exists(path) :
        with open(path,'r',encoding="utf8") as f :
            text = f.read()
        print(text)
    else :
        print(f"파일없음")
        
read_meet_code()
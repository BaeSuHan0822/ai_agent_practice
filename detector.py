import subprocess,os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

file_path = os.path.expanduser("~/Library/Mobile Documents/com~apple~CloudDocs/MeetBridge/latest_meet.txt")
dir_path = os.path.dirname(file_path)
total_text = ""

class Handler(FileSystemEventHandler) :
    def on_modified(self,event) :
        if not event.is_directory and event.src_path == file_path :
            print(f"파일 변경 감지됨 : {event.src_path}")
            read_meet_code()


def read_meet_code() :
    if os.path.exists(file_path) :
        with open(file_path,'r',encoding="utf8") as f :
            total_text = f.read()
    else :
        print(f"파일없음")
        
event_handler = Handler()
observer = Observer()
observer.schedule(event_handler,dir_path,recursive = False)

observer.start()
print(f"{dir_path} 파일 변화 감지 중....")

try :
    while True :
        time.sleep(1)
except KeyboardInterrupt :
    observer.stop()
    print("모니터링 종료")
    
observer.join()
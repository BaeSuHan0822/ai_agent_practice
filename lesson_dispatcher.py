import pyautogui
import time,json
import os,subprocess

def open_pdf(name : str) :
    with open('students.json','r',encoding="utf-8") as f :
        json_data = json.load(f)
        for student,path in json_data.items() :
            if name in student and os.path.exists(path) :
                subprocess.run(['open',path])
                print("파일이 열렸습니다.")
                        
    
open_pdf()
import threading 
import time 
import os 
import subprocess 
def get_process_count(imagename): 
    p = os.popen('tasklist /FI "IMAGENAME eq %s"' % imagename) 
    return p.read().count(imagename) 
def timer_start(): 
    t = threading.Timer(300,watch_func) 
    t.start() 
def watch_func(): 
    print "I'm watch_func is running..."
    if get_process_count('python.exe') == 0 : 
        print subprocess.Popen([r'C:\Users\jxy\Desktop\XDU-tower\a.bat']) 
    timer_start() 
if __name__ == "__main__": 
    timer_start() 
    while True: 
        time.sleep(1) 

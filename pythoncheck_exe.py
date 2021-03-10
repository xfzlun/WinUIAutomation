# python定时检查启动某个exe程序（如果exe挂了）
import threading
import time
import os
import subprocess
 
 
def get_process_count(imagename):
    p = os.popen('tasklist /FI "IMAGENAME eq %s"' % imagename)
    return p.read().count(imagename)
 
def timer_start():
    t = threading.Timer(120,watch_func,("is running..."))
    t.start()
    
def watch_func(msg):
    print "I'm watch_func,",msg
    if get_process_count('main.exe') == 0 :
        print subprocess.Popen([r'D:\shuaji\bin\main.exe'])
    timer_start()
    
if __name__ == "__main__":
    timer_start()
    while True:
        time.sleep(1)
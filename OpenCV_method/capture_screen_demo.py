#encoding=utf-8

import cv2
import threading
import time
flag_video = True
def videoCapture():
    print(cv2.__version__)
    print('cv2.VideoCapture......')
    global cap
    cap = cv2.VideoCapture(0)
    print('cap.read......')
    ret, frame = cap.read()
    
    global flag_video
    print('Open camera......')
    global flag_video
    while (flag_video):
        cv2.namedWindow('Video')
        cv2.imshow('Video', frame)
        cv2.waitKey(10)
        ret, frame = cap.read()
    print('Close camera......')
    cap.release()
videoCapture()
'''    
if __name__ == '__main__':
    t = threading.Thread(target=videoCapture, args=())
    t.start()
    time.sleep(10)
    flag_video 
    flag_video = False    
    time.sleep(10)
'''
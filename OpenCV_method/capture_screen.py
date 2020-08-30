#encoding = utf-8

import cv2
import time

def usbCamDetect():
    num = 0
    global cap
    cap = cv2.VideoCapture(num)

    while(num < 4):
        if cap.isOpened():
            print(num)
            cap.release()
            return num
        else:
            print('id %d has no cam detected...' % num)
            num += 1
    cap.release()



def screenCapture(num):
    if usbid != None:
        print(cv2.__version__)
        print('Screen Capturing>>>')
        #global cap
        #cap = cv2.VideoCapture(usbid)
        #codec = 0x47504A4D  # MJPG
        #cap.set(cv.CAP_PROP_FPS, 30.0)
        #cap.set(cv.CAP_PROP_FOURCC, codec)
        cap.open(num)
        cap.set(3,1280)#1024
        cap.set(4,720)#768
        print('Image reading>>>')
        #ret, frame = cap.read()
        global videoFlag
        print('Camera detecting...')
        videoFlag = cap.isOpened()
        while (videoFlag):
            #cv2.waitKey(1)
            ret, frame = cap.read()
            try:
                if ret:
                    print('saving pic.....')
                    picname = './capture.bmp'
                    cv2.imwrite(picname, frame)
                    break
                else:
                    print('No Image....')
                    break
            except IOError:
                print("Pic can not be saved")
                break
    else:
        print('No Camera detected!')
    print('Camera closing>>>')
    cap.release()

usbCamDetect()
screenCapture(num)

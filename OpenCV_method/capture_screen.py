#encoding = utf-8

import cv2
import time

def screenCapture(usbid):
    print(cv2.__version__)
    print('Screen Capturing>>>')
    global cap
    cap = cv2.VideoCapture(usbid)
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
    print('Camera closing>>>')
    cap.release()

screenCapture(0)
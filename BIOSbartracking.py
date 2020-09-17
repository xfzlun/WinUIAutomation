# -*- coding:utf-8 -*-

'''
主要要实现跟踪BIOS下的光标，截图，OCR识别
'''
import cv2
import numpy as np
import time
import matplotlib.pyplot as plt

bar_color = 'red'  # 选择想要识别的颜色

# HSV的取色范围设定如下，我们可以利用matplotlib的plt.show功能找出阀值
color_dist = {'red': {'Lower': np.array([0, 255, 58]), 'Upper': np.array([6, 255, 255])},
              'blue': {'Lower': np.array([100, 80, 46]), 'Upper': np.array([124, 255, 255])},
              'green': {'Lower': np.array([35, 43, 35]), 'Upper': np.array([90, 255, 255])},
              }

cap = cv2.VideoCapture(0)
cv2.namedWindow('camera', cv2.WINDOW_AUTOSIZE)
while cap.isOpened():
    ret, frame = cap.read()
    #cv2.imshow('test', frame)
    #cv2.waitKey(0) & 0xFF = ord('q')
    if ret:
        if frame is not None:
            gs_frame = cv2.GaussianBlur(frame, (5, 5), 0)                     # 高斯模糊
            hsv = cv2.cvtColor(gs_frame, cv2.COLOR_BGR2HSV)
            #plt.imshow(hsv)
            #plt.ion
            #plt.pause(10)
            #plt.close()
            # 转化成HSV图像
            erode_hsv = cv2.erode(hsv, None, iterations=2)                   # 腐蚀 粗的变细
            inRange_hsv = cv2.inRange(erode_hsv, color_dist[bar_color]['Lower'], color_dist[bar_color]['Upper'])
            #cv2.imshow("hsv", inRange_hsv)
            #cv2.waitKey(5)
            cnts = cv2.findContours(inRange_hsv.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
            time.sleep(2)
            c = max(cnts, key=cv2.contourArea)
            rect = cv2.minAreaRect(c)
            box = cv2.boxPoints(rect)
            cv2.drawContours(frame, [np.int0(box)], -1, (0, 255, 255), 2)

            cv2.imshow('camera', frame)
            cv2.waitKey(1)
        else:
            print("无画面")
    else:
        print("无法读取摄像头！")

cap.release()
cv2.waitKey(0)
cv2.destroyAllWindows()



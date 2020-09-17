# -*- coding:utf-8 -*-
'''
这是一个测试摄像头效果的脚本
'''
import cv2
import numpy as np
import matplotlib.pyplot as plt
import time
import os

cap = cv2.VideoCapture(0)
cap.set(3, 1920)
cap.set(4, 1080)

while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        if frame is not None:
            frame1 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            plt.imshow(frame1)
            plt.show()
            # 如果想要展示一段时间自动关闭显示，把plt.show()换成下面的代码
            #plt.ion
            #plt.pause(10)
            #plt.close()
            break
            #if cv2.waitKey(1) & 0xFF == ord('q'):
                #break
        else:
            print("No frame!!")
    else:
        print("无法读取摄像头")

cap.release()
cv2.destroyAllWindows()
import numpy as np
import cv2

# 测试摄像头
cap = cv2.VideoCapture(0)

while (True):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('frame', gray)
    if cv2.waitKey(1) &0xff == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
'''
1）首先创建一个VideoCapture 对象。他的参数可以是设备的索引号，或者是一个视频文件。设备索引号就是在指定要使用的摄像头。 
一般的笔记本电脑都有内置摄像头。所以参数就是0。 
2）cap.read() 返回一个布尔值（True/False）。如果帧读取的是正确的，返回True 
3）cvtColor为颜色空间转换函数，可以实现RGB颜色向HSV,HSI等颜色空间的转换，也可以转换为灰度图像。第二个参数CV_BGR2GRAY表示转换为灰度图，CV_BGR2HSV将图片从RGB空间转换为HSV空间
'''

# 接下来请参考 自动化测试-利用OpenCV进行图像识别定位


# -*- coding: utf-8 -*-

import cv2 as cv
from aip import AipOcr
import matplotlib.pyplot as plt
import time

#调用摄像头
ID = 0   #指定摄像头的USBID，这个在windows底下要怎吗查询？
cap = cv.VideoCapture(ID)  # 创建一个VideoCapture的实例对象
if not cap.isOpened():  #检查摄像头是否开启
    print("Camera cannot be opened") #如果摄像头没有被开启，则弹出提示后离开程序
    exit(0) # 离开程序



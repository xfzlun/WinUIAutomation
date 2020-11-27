# -*- coding: utf-8 -*-

import cv2 as cv
from aip import AipOcr
import matplotlib.pyplot as plt
import time, sys, os

#调用摄像头
ID = 0   #指定摄像头的USBID，这个在windows底下要怎吗查询？
cap = cv.VideoCapture(ID)  # 创建一个VideoCapture的实例对象
if not cap.isOpened():  #检查摄像头是否开启
    print("Camera cannot be opened") #如果摄像头没有被开启，则弹出提示后离开程序
    exit(0) # 离开程序，参见底下备注

while True:
    ret, frame = cap.read()  #调用read方法，从我们的VideoCapture实例对象读取一帧画面
    if not ret:
        print("Can't receive frame, Exiting.....")
        break
    # Here comes the operation we need to do on the frame
    gray = cv.cvtColor()

'''
备注：
Python中exit()的用法
Python中分成几种，
1. sys.exit(n) : 退出程序引发SystemExit异常，可以捕获异常执行些清理工作，sys.exit()会引发一个异常：SystemExit，这是唯一一个不会被认为是错误的异常。
                n默认值为0,表示正常退出，其他都是非正常退出，也可以用sys.exit("Sorry, Goodbye"). 一般在主程序中，我们用此方式退出
                如果这个异常没有被捕获，那么python解释器将会退出。如果有捕获此异常的代码，那么这些代码还是会执行。捕获这个异常可以做一些额外的清理工作。n默认值为0，0为正常退出，其他数值（1-127）为不正常，可抛异常事件供捕获。一般主程序中使用此退出。
                SystemExit 并不派生自Exception 所以用Exception捕捉不到该SystemEixt异常，应该使用SystemExit来捕捉。
2. os.exit(n): 直接退出，不抛异常，不执行相关清理工作，常用在子进程的退出
3. exit()/quit() ： 直接抛出SystemExit异常，一般在交互式shell中退出使用

在很多操作系统中，exit(0)可以中断某个程序，括号中的数字表示是否碰到错误而中断，exit(1)表示发生了错误，而exit(0)则表示程序是正常退出的，与布尔逻辑中 0 == False相反
'''




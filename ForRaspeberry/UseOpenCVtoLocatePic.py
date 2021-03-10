# 自动化测试 - 利用OpenCV进行图像识别与定位
import cv2
#读取图片，以1.png为例
img = cv2.imread('MyPic.jpg')
sift = cv2.xfeatures2d.SIFT_create()  #检测关键点并计算描述


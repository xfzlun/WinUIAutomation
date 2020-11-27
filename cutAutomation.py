#-*- coding:utf-8 -*-

import cv2
import os
import time
import numpy as np
import matplotlib.pyplot as plt
import imutils

'''
1. 辨识BIOS光标位置  两个方案：1. 颜色识别，2. 轮廓识别
'''

picPath = "C:\\Users\\Laurence_SZH\\Pictures\\Camera Roll\\201124183637.BMP"
fullPath = os.path.expanduser(picPath)
print(fullPath)

pic = cv2.imread(fullPath)
print(pic)
#pic2 = pic[:,:,[2,1,0]] 
pic2 = cv2.cvtColor(pic, cv2.COLOR_BGR2RGB)
#plt.subplot(20, 20, 10)
#以下这段主要是show出我们读到的图片

#用plt.show的好处是可以读得到threshod的值
plt.imshow(pic2)
plt.title('BGR')
#plt.show()  # 用这个会一直显示
plt.ion()  #搭配plt.pause & plt.close()可以让窗口显示5秒就关闭
plt.pause(5)  
#plt.waitforbuttonpress(4)
plt.close()  #关闭图像窗口

# 利用阀值_绘制长方形的BIOS光标轮廓
img_gray = cv2.cvtColor(pic, cv2.COLOR_BGR2GRAY)
# ret, thresh = cv2.threshold(img_gray, 16, 18, 0)
ret, thresh = cv2.threshold(img_gray, 33, 0, 0)
plt.imshow(img_gray)
plt.title('thresh')
plt.ion()  
plt.pause(35)
plt.close()

#检测图像的连通区(输入为二值化图像)
threshold, contours, heirarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# 绘制寻找到的轮廓线
img_contours = cv2.drawContours(pic, contours, -1, (255,255,255),3)

cv2.imshow('contours', img_contours)
cv2.waitKey(0) & 0xFF == ord('q')

# 测试一下那个阀值的参数更适合我们的BIOS介面
#import numpy as np
#from matplotlib import pyplot as plt

#img = cv2.imread(r'/Users/Documents/image01.jpg',0)   # 读入灰度图
ret,thresh1 = cv2.threshold(img_gray,127,255,cv2.THRESH_BINARY)
ret,thresh2 = cv2.threshold(img_gray,127,255,cv2.THRESH_BINARY_INV)
ret,thresh3 = cv2.threshold(img_gray,127,255,cv2.THRESH_TRUNC)
ret,thresh4 = cv2.threshold(img_gray,127,255,cv2.THRESH_TOZERO)
ret,thresh5 = cv2.threshold(img_gray,127,255,cv2.THRESH_TOZERO_INV)

titles = ['Original Image','BINARY','BINARY_INV','TRUNC','TOZERO','TOZERO_INV']
images = [img_gray, thresh1, thresh2, thresh3, thresh4, thresh5]

for i in range(6):
    plt.subplot(2,3,i+1),plt.imshow(images[i],'gray')
    plt.title(titles[i])
    plt.xticks([]),plt.yticks([])

plt.show()



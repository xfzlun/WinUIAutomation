# -*- coding:utf-8 -*-
'''
轮廓 可以简单地解释为 连接具有相同颜色或强度的所有连续点（沿边界）的曲线。轮廓是用于 形状分析 以及 对象检测和识别 的有用工具。

轮廓相关的注意事项：
为了获得更高的准确性，请使用二进制图像（binary images）。因此，在找到轮廓之前，
请应用阈值（threshold ）或 Canny边缘检测（canny edge detection）；
调用cv2.findContours()函数、cv2.drawContours()函数将修改源图像。
因此，如果想在找到轮廓后仍可获取源图像，需保证在调用findContours()函数、
cv2.drawContours()函数之前已经将其存储到其他变量中；
在OpenCV中，寻找图像轮廓类似于从黑色背景中找到白色物体。
因此，请记住，要找到的对象应该是白色，背景应该是黑色。

使用OpenCV的findContours获取轮廓并切割(python)  -- Line 9
https://blog.csdn.net/loovelj/article/details/78739790
基于Python+OpenCV自动提取并裁切ROI（感兴趣区域） -- Line 54
https://blog.csdn.net/weixin_43181409/article/details/104778084
'''

import cv2
import numpy as np

img =cv2.imread("./result.png")
'''
#1 获取轮廓
OpenCV2获取轮廓主要是用cv2.findContours
cv2.findContours(img, mode, method)
img	输入的原图片
mode 轮廓检索模式
RETR_EXTERNAL ：只检索最外面的轮廓；
RETR_LIST：检索所有的轮廓，并将其保存到一条链表当中；
RETR_CCOMP：检索所有的轮廓，并将他们组织为两层：顶层是各部分的外部边界，第二层是空洞的边界;
RETR_TREE：检索所有的轮廓，并重构嵌套轮廓的整个层次;

method	轮廓逼近模式
CHAIN_APPROX_NONE：以Freeman链码的方式输出轮廓，所有其他方法输出多边形（顶点的序列）。
CHAIN_APPROX_SIMPLE：压缩水平的、垂直的和斜的部分，也就是，函数只保留他们的终点部分。
'''
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # 转成灰度
ret, binary = cv2.threshold(gray, 15, 255,cv2.THRESH_BINARY)
img_binary = cv2.imwrite('./result_binary2.png', binary)
#image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) 旧版本返回三个参数，新版本返回2个
contours, hierarchy = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
'''
findContours的第二个函数很重要，主要分为 cv2.RETR_LIST, cv2.RETR_TREE, cv2.RETR_CCOMP, cv2.RETR_EXTERNAL，具体含义可参考官方文档
'''
import numpy as np
import matplotlib.pyplot as plt
import cv2

img = cv2.imread(r'/Documents/2d36d7c607b0f923a9aa3ef1a7b274cb.jpg')
# 转为灰度图
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# 把原图二值化——选取一个全局阈值`thresh`，然后根据全局阈值将一幅灰度图二值化，
# 将灰度图img中灰度值小于阈值的点置0，灰度值大于175的点置255
ret, thresh = cv2.threshold(img_gray, 127, 255, 0)
# 检测图像连通区（输入为二值化图像）
contours, heirarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) 
# 绘制寻找到的轮廓线（在原始图像上绘制轮廓线）
img_contours = cv2.drawContours(img, contours, -1, (0,255,0), 3)
plt.imshow(img_contours)



'''
#2 画出轮廓
为了看到自己画了哪些轮廓，可以使用 cv2.boundingRect()函数获取轮廓的范围，即左上角原点，以及他的高和宽。然后用cv2.rectangle()方法画出矩形轮廓
'''
for i in range(0,len(contours)):  
	x, y, w, h = cv2.boundingRect(contours[i])   
	cv2.rectangle(image, (x,y), (x+w,y+h), (153,153,0), 5) 

'''
#3 切割轮廓
轮廓的切割主要是通过数组切片实现的，不过这里有一个小技巧：就是图片切割的w,h是宽和高，而数组讲的是行（row）和列（column）
所以，在切割图片时，数组的高和宽是反过来写的
'''
   newimage=image[y+2:y+h-2,x+2:x+w-2] # 先用y确定高，再用x确定宽
            nrootdir=("E:/cut_image/")
            if not os.path.isdir(nrootdir):
                os.makedirs(nrootdir)
            cv2.imwrite( nrootdir+str(i)+".jpg",newimage) 
            print (i)

'''
轮廓绘制
OpenCV函数原型
cv2.drawContours(image, contours, contourIdx, color, thickness)

参数解释
image	输入的原图片
contours	已经查找出的多个轮廓
contourldx	需要绘制的轮廓的索引
color	绘制的颜色
thickness	绘制的粗细，如果该参数小于0，则表示填充整个轮廓内的区域
注意：该函数会直接在图片上进行绘制，所以一般要将原图复制一份，再进行绘制
'''
cv2.drawContours(img,contours,-1,(0,0,255),3)
cv2.imwrite("img_draw.png", img)


print(len(contours))
print(contours)

'''
轮廓特征
令cnt为图像中的一个轮廓
'''
binary, contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
cnt = contours[8]
cv2.contourArea(cnt)  #计算面积
cv2.arcLength(cnt, True)  # 计算周长  注意：第二个参数指定图形是否闭环,如果是则为True, 否则只是一条曲线。
'''
轮廓近似
OpenCV函数原型
cv2.approxPolyDP(curve, epsilon, closed)
参数解释
curve	需要进行近似的轮廓
epsilon	指定近似精度的参数ε，这是原始曲线与其近似值之间的最大距离。参数越小，两直线越接近
closed	若为true，曲线第一个点与最后一个点连接形成闭合曲线，若为false，曲线不闭合。

轮廓的外接矩形
OpenCV函数原型
cv2.rectangle(img, (x, y), (x + w, y + h), color, thickness)
参数解释
img	进行绘制的图片
x,y	轮廓左上角的坐标
w,h	轮廓的宽度和高度
color	轮廓颜色
thickness	轮廓线条的粗细
关于x,y,w,h的位置关系
'''
x,y ------
|          |
|          |
|          |
--------x+w,y+h

'''
opencv for python (19) 根据矩进行形状匹配
函数 cv2.matchShape() 可以帮我们比较两个形状或轮廓的相似度。
如果返回值越小，匹配越好。它是根据 Hu 矩来计算的。Hu 矩是归一化中心矩的线性组合，
之所以这样做是为了能够获取代表图像的某个特征的矩函数，这些矩函数对某些变化如缩放，旋转，镜像映射具有不变形。
'''
# 根据矩进行形状匹配
import cv2
import numpy as np

img1 = cv2.imread('t1_re.png',0)
img2 = cv2.imread('t1_re2.png',0)
img3 = cv2.imread('t1_.png',0)

ret,thresh = cv2.threshold(img1,127,255,0)
ret2,thresh2 = cv2.threshold(img2,127,255,0)
ret3,thresh3 = cv2.threshold(img3,127,255,0)
contours,hierarchy = cv2.findContours(thresh,2,1)
cnt1 = contours[0]
contours2,hierarchy2 = cv2.findContours(thresh2,2,1)
cnt2 = contours2[0]
contours3,hierarchy3 = cv2.findContours(thresh3,2,1)
cnt3 = contours3[0]

ret = cv2.matchShapes(cnt1,cnt2,1,0.0)
ret1 = cv2.matchShapes(cnt1,cnt3,1,0.0)
ret2 = cv2.matchShapes(cnt1,cnt1,1,0.0)

print ret,ret1,ret2


#范例代码：
import cv2 as cv
import numpy as np
 
# 读入图片
src = cv.imread('contours.png')
# 转换成灰度图
gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY)
# 二值化
ret, thresh = cv.threshold(gray, 129, 255, cv.THRESH_BINARY)
 
# 查找轮廓
# binary-二值化结果，contours-轮廓信息，hierarchy-层级
binary, contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
# 显示轮廓，tmp为黑色的背景图
tmp = np.zeros(src.shape, np.uint8)
res = cv.drawContours(tmp, contours, -1, (250, 255, 255), 1)
cv.imshow('Allcontours', res)
 
cnt = contours[8]
tmp2 = np.zeros(src.shape, np.uint8)
res2 = cv.drawContours(tmp2, cnt, -1, (250, 255, 255), 2)
cv.imshow('cnt', res2)
 
# 轮廓特征
# 面积
print(cv.contourArea(cnt))
# 周长,第二个参数指定图形是否闭环,如果是则为True, 否则只是一条曲线.
print(cv.arcLength(cnt, True))
 
# 轮廓近似，epsilon数值越小，越近似
epsilon = 0.08 * cv.arcLength(cnt, True)
approx = cv.approxPolyDP(cnt, epsilon, True)
tmp2 = np.zeros(src.shape, np.uint8)
# 注意，这里approx要加中括号
res3 = cv.drawContours(tmp2, [approx], -1, (250, 250, 255), 1)
cv.imshow('approx', res3)
 
# 外接图形
x, y, w, h = cv.boundingRect(cnt)
# 直接在图片上进行绘制，所以一般要将原图复制一份，再进行绘制
tmp3 = src.copy()
res4 = cv.rectangle(tmp3, (x, y), (x + w, y + h), (0, 0, 255), 2)
cv.imshow('rectangle', res4)
 
cv.waitKey()
cv.destroyAllWindows()

'''
主要记录一下自己在找资料并实现的过程
一、基本思路
二、代码实例
一、基本思路
通过OpenCV读取图片，进行二值化操作后寻找轮廓，并且将轮廓保存再与原图片进行位与运算，完成裁切效果。本项目中主要提取图片中的圆形以及三角形。

二、代码实例
'''
import cv2 as cv
import numpy as np


src = cv.imread(r"D:\test5.jpg") # 读取图片
ROI = np.zeros(src.shape, np.uint8) # 创建与原图同尺寸的空numpy数组，用来保存ROI信息

gray = cv.cvtColor(src, cv.COLOR_BGR2GRAY) # 灰度化
ret, binary = cv.threshold(gray,
			   0, 255, 
			   cv.THRESH_BINARY_INV | cv.THRESH_TRIANGLE) # 自适应二值化
			   
out_binary, contours, hierarchy = cv.findContours(binary, 
			   cv.RETR_EXTERNAL,
			   cv.CHAIN_APPROX_SIMPLE) # 查找所有轮廓，每个轮廓信息保存于contours数组中

for cnt in range(len(contours)): # 基于轮廓数量处理每个轮廓
    # 轮廓逼近，具体原理还需要深入研究
    epsilon = 0.01 * cv.arcLength(contours[cnt], True)
    approx = cv.approxPolyDP(contours[cnt], epsilon, True) # 保存逼近结果的顶点信息
    							   # 顶点个数决定轮廓形状 
    # 计算轮廓中心位置							   
    mm = cv.moments(contours[cnt])
    if mm['m00'] != 0:
        cx = int(mm['m10'] / mm['m00'])
        cy = int(mm['m01'] / mm['m00'])
        color = src[cy][cx]
        color_str = "(" + str(color[0]) + ", " + str(color[1]) + ", " + str(color[2]) + ")"
        p = cv.arcLength(contours[cnt], True)
        area = cv.contourArea(contours[cnt])
        
        # 分析几何形状
        corners = len(approx)
        if corners == 3 and (color[2]>=150 or color[0]>=150) and area>1000:  # 一系列判定条件是由该项目的特点所调整的
            cv.drawContours(ROI, contours, cnt, (255, 255, 255), -1)  # 在ROI空画布上画出轮廓，并填充白色（最后的参数为轮廓线条宽度，如果为负数则直接填充区域）
            imgroi = ROI & src  # ROI和原图进行与运算，筛出原图中的ROI区域
            cv.imshow("ROI", imgroi)
            cv.imwrite(r"D:\ROI.jpg")
            
        if corners >= 10 and (color[2]>=150 or color[0]>=150) and area>1000:          
    	    cv.drawContours(ROI, contours, cnt, (255, 255, 255), -1)
            imgroi = ROI & src
            cv.imshow("ROI",imgroi）
            cv.imwrite(r"D:\ROI.jpg")

            
cv.waitKey(0)
cv.destroyAllWindows()         



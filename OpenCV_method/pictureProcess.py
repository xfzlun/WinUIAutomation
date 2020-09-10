import cv2
import os
import time
import numpy as np
import matplotlib.pyplot as plt
import imutils

picPath = '~/testcapture.png'  #标明图片档案所在位置
fullPath = os.path.expanduser(picPath)  #
print(fullPath)
#读入图像
pic1 = cv2.imread(fullPath) #读取图档用imread, 但是如果是用摄像头截取的实例对象，就可以用 对象.read()方法读取，例如：cap.read()
#frame = imutils.resize(pic1, width = 640)
#lt.imshow(imutils.opencv2matplotlib(pic1))
#cv2.waitKey(0) & 0xFF == ord('q')
#plt.imwrite()

#以下3行不知道为什么MAC show不出来
plt.subplot(2, 2, 1)  
plt.imshow(pic1)
plt.title('BGR')

'''
while(True):
    cv2.imshow("test", pic1)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
'''

#颜色空间转换, 一般应用以转灰度为主
pic_RGB = cv2.cvtColor(pic1, cv2.COLOR_BGR2RGB)
pic_Gray = cv2.cvtColor(pic1, cv2.COLOR_BGR2GRAY)
pic_HSV = cv2.cvtColor(pic1, cv2.COLOR_BGR2HSV)
cv2.imwrite('./pic_RGB.png', pic_RGB)
cv2.imwrite('./pic_Gray.png', pic_Gray)
cv2.imwrite('./pic_HSV.png', pic_HSV)

'''
cv2.inRange()提取图片中指定颜色
将一副图像从rgb颜色空间转换到hsv颜色空间，颜色去除白色背景部分
具体步骤如下，调用了cv2的两个函数：
1. rgb转hsv的函数, 就是上面提到的cv2.cvtColor(pic1, cv2.COLOR_BGR2HSV)
2. 然后利用cv2.inRange函数设阈值，去除背景部分
  mask = cv2.inRange(hsv, lower_red, upper_red) #lower20===>0,upper200==>0,
'''
hsv_pic = cv2.cvtColor(pic1, cv2.COLOR_BGR2HSV)
lower_red = np.array([0, 43, 46])
upper_red = np.array([10, 255, 255])
# 如果想要留下红色的怎么设置？？
mask_pic = cv2.inRange(hsv_pic, lower_red, upper_red)
cv2.imwrite('./pic_mask.png', mask_pic)
cv2.imshow('pic_mask', mask_pic)
cv2.waitKey(0) & 0xFF == ord('q')
cv2.destroyAllWindows()

'''
核心功能：就是将低于lower_red和高于upper_red的部分分别变成0，lower_red～upper_red之间的值变成255
函数很简单，参数有三个
第一个参数：hsv指的是原图
第二个参数：lower_red指的是图像中低于这个lower_red的值，图像值变为0
第三个参数：upper_red指的是图像中高于这个upper_red的值，图像值变为0
而在lower_red～upper_red之间的值变成255
'''
'''
openCV+Python 数字图像处理（1）——图像基本操作（读入显示保存、属性读取、均值标准差、取反、色彩空间转换、提取颜色、通道分离与合并）
'''
import cv2
import numpy as np

# 1.读入图片和保存图片
img1 = cv2.imread('E:/PycharmProjects/one.jpg')

# 2.显示图片
def show(name, img):
    cv2.imshow(name, img)
    cv2.waitKey(0)
show('img1', img1)

# 3.保存图像
cv2.imwrite('E:/PycharmProjects/one.png', img1)

# 4.获取图片属性
def img_info(img):
    print('type:', type(img))
    print('img.size:', img.size)
    print('img.dtype:', img.dtype)
    print('img.shape', img.shape)
img_info(img1)

# 5.图像求均值、标准差
def mean_dev(img):
    mean_img = cv2.mean(img)
    print('mean', mean_img)
    m, stddev = cv2.meanStdDev(img)
    print('m', m, '\n', 'StdDev', stddev)
mean_dev(img1)

# 6.遍历图像各个像素且取反(有问题)
def reverse_img(img):
    h, w, c = img.shape
    r_img = np.zeros([h, w, c])
    for row in range(h):
        for col in range(w):
            for ch in range(c):
                r_img[row, col, ch] = 255-img[row, col, ch]
    show('reverse_img', r_img)

# reverse_img(img1)

# 7.openCV取反函数
def not_img(img):
    not_img = cv2.bitwise_not(img)
    show('not_img', not_img)
not_img(img1)

# 8.图像色彩空间转换
def color_cvt_img(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    show('gray', gray)
    show('hsv', hsv)
color_cvt_img(img1)

# 9.对图片的某种颜色进行提取
def color_inrange(img):
    low = np.array([0, 0, 0])
    up = np.array([255, 100, 100])
    blue_img1 = cv2.inRange(img1, low, up)
    show('blue_img1', blue_img1)
color_inrange(img1)


# 10.通道分离、合并
def img_channel(img):
    b, g, r = cv2.split(img)
    show('blue', b)
    print('blue.shape', b.shape)
    merge_img = cv2.merge([b, g, r])
    show('merge_img', merge_img)
img_channel(img1)



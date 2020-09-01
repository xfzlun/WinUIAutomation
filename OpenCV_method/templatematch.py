'''
OpenCV模版匹配
1. 根据特定的图像模版，在整个图像区域找寻匹配的图像，并生成区域位置讯息，方便后续鼠标或是键盘的操作
2. 需要一个模版图像
3. 待测的图像对象
4. 在待测的图像的左上开始，左到右，上到下搜寻并进行匹配
5. 计算模版图像与重叠的子图像的模版匹配度
6. 匹配度越高，两者相同的可能性越大
'''
import cv2 as cv
import numpy as np
def template_demo():
    tpl = cv2.imread("C:\\xxxx\\xxx\\template.png") #这里放入template图像的位置
    target = cv2.imread("C:\\xxx\\xxx\\target.png") #指定目标图像的位置，也可以用capture方法取得桌面截图赋值给target对象
    cv.imshow('tpl', tpl)  
    cv.imshow('target', target)
    methods = [cv.TM_SQDIFF_NORMED, cv.TM_CORR_NORMED, cv.TM_CCOEFF_NORMED]
    th, tw = tpl.shape[:2]
    for md in methods:
        print(md)
        result = cv.matchTemplate(target, tpl, md)
        min_val, max_val, min_loc, max_loc = cv.mixMaxLoc(result)
        if md == cv.TM_SQDIFF_NORMED:
            tl = min_loc
        else:
            tl = max_loc
        br = (tl[0]+tw, tl[1]+th)
        cv.rectangle(target, tl, br, (0,0,255), 2)
        cv.imshow("match"+np.str(md), target)

template_demo()
cv.waitkey(0)
cv.destroyAllWindow()


'''
#定义一个函数，检测图像是否开启
def capture():
    imgCapture = ImageGrab.grab() #ImageGrab应该是另一个桌面截图的对象
    imgConvert = cv2.cvtColor(np.asarray(imgCapture), cv2.COLOR_RGB2BGR)  # 转换成cv2格式
    os.chdir('C:/Users/')  # 输入范例图片所在的资料夹
    imgRead = cv2.imread('monster_1.png')  # ac应该是不需要的，这不知道又是那个对象 
    matchResult = cv2.matchTemplate(imgConvert, imgRead, cv2.TM_CCOEFF_NORMED) #用TM_SQDIFF_NORMED方式匹配
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(matchResult)  #在结果中取出坐标
    pt = max_loc
    mminpos = cv2.matchTemplate(imgConvert, imgRead, cv2.TM_SQDIFF_NORMED)
    nmin_val, nmax_val, nmin_loc, nmax_loc = cv2.minMaxLoc(mminpos)  #在结果中取出坐标
    minpt = nmin_loc
    if pt == minpt:
        print(pt)
        print(minpt)
        return pt  #左上角的坐标
    else:
        return None
'''


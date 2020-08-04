'''
用Pywinauto在windows下實現截圖，切割，定位圖片位置，自動移動鼠標過去點擊該位置
'''

import pyautogui
import random
import pyperclip

#截图
pyautogui.screenshot('screenshot_desktop.png')  #截全屏
pyautogui.screenshot('screenshot_part.png',region=(0,0,300,400))  # 指定区域(从0，0开始截取x方向为300px，y方向为400px的一张图切割



#find target pic
Part = pyautogui.locateOnScreen('screenshot_part.png', confidence=0.9)  
#('screenshot_part.png',confidence=0.9) 不知道为什么加了精度参数confidence以后就一直报错
#查詢文檔以後發現(文档位置: https://pyautogui.readthedocs.io/en/latest/)
#解决方案：需要在环境中安装OpenCV,原话是 Note: You need to have OpenCV installed for the confidence keyword to work.
abc=pyautogui.center(Part)  #查找图片的中心点
print(abc)

'''
There are following methods for locating target pic. 
1. locateOnScreen(image): return the first matched instance on screen
2. locateCenterOnScreen(image): return the center location of the first matched image on screen.
3. locateAllOnScreen(image)： return generator??
'''
print(pyautogui.locateAllOnScreen('screenshot_part.jpg'))

# speed up locate target pic.
#tips: region: 缩小查找区域
pyautogui.locateOnScreen('screenshot_part.png', region=(0, 0, 600, 800))

#tips2:灰度匹配，可提升找图速度
pyautogui.locateOnScreen('screenshot_part.png', grayscale=True)

# 取点
# 单个像素点颜色匹配，传入一个坐标返回该坐标的RGB值
# 方法一：实例化一个对象
im = pyautogui.screenshot()
print(type(im), im.getpixel((100,200)))  # getpixel传入一个元祖类型的参数，话说这里getpixel(100,200)是啥意思啊
#应该跟方法2的目的是一样的吧
#方法2
pix = pyautogui.pixel(100,200) #获取指定x,y的RGB值
print(pix)

#RGB值匹配
#单个像素点与给定像素匹配，给定像素点以Tuple的形式
print(pyautogui.pixelMatchesColor(100, 200, (41, 128, 185)))
# tolerance关键字参数，可在一定误差内进行匹配
print(pyautogui.pixelMatchesColor(100, 200, (25, 118, 199), tolerance=20))

# 可以做多点匹配，将坐标传入数组，然后循环比色即可(这个功能不确定能不能用来测试AC)




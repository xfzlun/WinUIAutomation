'''
用Pywinauto在windows下實現截圖，切割，定位圖片位置，自動移動鼠標過去點擊該位置
'''

import pyautogui
import random
import pyperclip

#截图
pyautogui.screenshot('screenshot_desktop.png')  #截全屏
pyautogui.screenshot('screenshot_part.png',region=(0,0,300,400))  # 指定区域切割


#find target pic
Part = pyautogui.locateOnScreen('screenshot_part.png')  
#('screenshot_part.png',confidence=0.9) 不知道为什么加了精度参数confidence以后就一直报错
#查詢文檔以後發現(文档位置: https://pyautogui.readthedocs.io/en/latest/)
#需要在环境中安装OpenCV,原话是 Note: You need to have OpenCV installed for the confidence keyword to work.
abc=pyautogui.center(Part)
print(abc)

'''
There are following methods for locating target pic. 
1. locateOnScreen(image): return the first matched instance on screen
2. locateCenterOnScreen(image): return the center location of the first matched image on screen.
3. locateAllOnScreen(image)： return generator??
'''
print(pyautogui.locateAllOnScreen('screenshot_part.jpg'))

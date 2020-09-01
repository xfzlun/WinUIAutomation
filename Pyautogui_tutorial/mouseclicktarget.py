import pyautogui
import random
import pyperclip

#左键点击脚本
def left_click(path): #定义一个函数实现左键点击的功能
    left_click1 = pyautogui.locateOnScreen(path) #把目标图片当作参数传递给path
    print('left_click1::', left_click1)
    if left_click1:
        url_x, url_y = pyautogui.center(left_click1)
        pyautogui.leftClick(url_x, url_y)
        return True
    return False


def change_ua(): #定义一个函数实现随机变换目标图片
    ua=random.choice(useragents)
    for i in range(2):
        result0 = left_click('./images/ua{}.png'.format(i))
        if result0:
            break
        result2 = left_click('./images/ua2.png')
        result3 = left_click('./images/ua3.png')
        result4 = left_click('./images/ua40.png')
        for j in range(1,3):
            result5 = left_click('./images/ua4{}.png'.format(j))
            if result5:
                pyautogui.hotkey('ctrl','a')
                pyautogui.hotkey('backspace')
                pyperclip.copy(ua)
                pyautogui.hotkey('ctrl','v')
                pyautogui.press('enter')
        result6 = left_click('./images/ua_refresh.png')
        left_click('./images/ua5.png')#左键点击脚本
def left_click(path): #定义一个函数实现左键点击的功能
    left_click1 = pyautogui.locateOnScreen(path) #把目标图片当作参数传递给path
    print('left_click1::', left_click1)
    if left_click1:
        url_x, url_y = pyautogui.center(left_click1)
        pyautogui.leftClick(url_x, url_y)
        return True
    return False


def change_ua(): #定义一个函数实现随机变换目标图片
    ua=random.choice(useragents)
    for i in range(2):
        result0 = left_click('./images/ua{}.png'.format(i))
        if result0:
            break
        result2 = left_click('./images/ua2.png')
        result3 = left_click('./images/ua3.png')
        result4 = left_click('./images/ua40.png')
        for j in range(1,3):
            result5 = left_click('./images/ua4{}.png'.format(j))
            if result5:
                pyautogui.hotkey('ctrl','a')
                pyautogui.hotkey('backspace')
                pyperclip.copy(ua)
                pyautogui.hotkey('ctrl','v')
                pyautogui.press('enter')
        result6 = left_click('./images/ua_refresh.png')
        left_click('./images/ua5.png')
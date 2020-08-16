import pyautogui

# 以正方形的形式，移动鼠标20次
for i in range(20): #for loop 实现移动20次
    pyautogui.moveTo(100, 100, duration = 3)
    pyautogui.moveTo(100, 200, duration = 3)
    pyautogui.moveTo(200, 200, duration = 3)
    pyautogui.moveTo(200, 100, duration = 3)


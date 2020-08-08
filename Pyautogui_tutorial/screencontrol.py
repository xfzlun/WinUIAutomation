#截屏
import pyautogui
img = pyautogui.screenshot()
img.save('img.png')

#截取指定位置，大小的图片
img = pyautogui.screenshot(region=[10,20,30,40])  #x,y,w,h
img.save('test.png')

#查找图片所在位置，点击
img_location = pyautogui.locateOnScreen(image='img.png')
logging.info("img location %s", img_location)  #这个是一个log讯息的概念？

if img_location:
    # 获取图片的中心位置，然后点击
    x, y = pyautogui.center(img_location)
    pyautogui.moveTo(x, y, duration=1)
    pyautogui.click()
    logging.info("click img_location...")



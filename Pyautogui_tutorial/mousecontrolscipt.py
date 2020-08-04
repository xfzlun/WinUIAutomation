import pyautogui as pg

# 间隔2秒钟将鼠标移动到坐标为100，100的位置
pg.FAILSAFE = False    #关掉保护措施，不设置会报下面附录的错误
pg.moveTo(x=100, y=100, duration=2)
pg.click()  #鼠标左键点击一次, 这个函数有很多参数，参见以下，可以玩看看
#pg.click(x=None, y=None, clicks=1, interval=0.0, button='left', duration=0.0, tween=pg.linear)


'''
第一次执行的时候报了这个错误，搜了一下貌似要关掉
Exception has occurred: FailSafeException
PyAutoGUI fail-safe triggered from mouse moving to a corner of the screen. To disable this fail-safe, set pyautogui.FAILSAFE to False. DISABLING FAIL-SAFE IS NOT RECOMMENDED.
  File "F:\codehub\WInAutomation\Pyautogui_tutorial\mousecontrolscipt.py", line 4, in <module>
    pg.moveTo(x=100, y=100, duration=2)
'''

# 鼠标移动到相对位置
# 用2秒钟的时间，将鼠标移动到现在鼠标所在位置的相对移动，向右移动10，向下移动10
pg.move.Rel(xOffset=10, yOffset=10, duration = 2)

#一般不用pyautogui.click()这个函数，因为记不住参数，使用下面封装好的参数比较快

#双击
pg.doubleClick()

#triple click

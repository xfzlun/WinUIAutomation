import pyautogui as pg

# 间隔2秒钟将鼠标移动到坐标为100，100的位置
pg.FAILSAFE = False    #设置保护措施，不设置会报下面附录的错误
pg.moveTo(x=100, y=100, duration=2)
pg.click()  #鼠标左键点击一次

'''
第一次执行的时候报了这个错误，搜了一下貌似要关掉
Exception has occurred: FailSafeException
PyAutoGUI fail-safe triggered from mouse moving to a corner of the screen. To disable this fail-safe, set pyautogui.FAILSAFE to False. DISABLING FAIL-SAFE IS NOT RECOMMENDED.
  File "F:\codehub\WInAutomation\Pyautogui_tutorial\mousecontrolscipt.py", line 4, in <module>
    pg.moveTo(x=100, y=100, duration=2)
'''
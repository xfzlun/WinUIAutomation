# 此程序主要是要实现当鼠标移动到任何点的时候，实时显示鼠标当前位置
# 程式需要实现以下功能：
# 1. 获得当前鼠标的(x,y)坐标 - 利用pyautogui.position函数
# 2. 当鼠标在屏幕上移动的时候，实时更新鼠标的坐标
# 3. 屏幕打印目前鼠标位置后，再下一个更新前要对目前已经打印出来的屏幕位置进行删除
# 4. 处理异常，方便用户退出程序
import pyautogui

print('Press Ctrl-C to quit') # 提示用户如何退出程序

try:
    while True: #利用while循环实现不断打印鼠标目前位置
        x, y = pyautogui.position()
        positionStr = 'X: ' + str(x).rjust(4) + 'Y: ' + str(y).rjust(4)  #格式化字符串，其中rjust函数实现将获取到的(x,y)坐标固定占据同样4个字符的宽度，再连接前面设定的字符串标签，保存在positionStr变数中
        print(positionStr, end='')  #打印鼠标目前位置，末尾的end=''表示阻止python中print函数默认的换行动作. 
        print('\b' * len(positionStr), end='', flush=True) # \b实现退格删除刚刚我们获取的positionStr的字串长度, flush=True的用途
except KeyboardInterrupt:  # 利用try-except以及KeyboardInterrupt实现当用户按下Ctrl-C的时候退出程序
    print('\nDone.')

# Pyautogui Tutorial

## Introduction

官方文档：http://pyautogui.readthedocs.org

参考书目：

1. Python编程快速上手---让繁琐的工作自动化   CH18

Pyatugui 是一个在Windows， Linux， OS X上面发送虚拟键盘按键与鼠标点击讯号，并且透过截图，找图功能实现上述作业系统中GUI的自动化操作，

## 环境准备

- Windows: 直接利用pip，不需要其他模块
- OS X: pip install pyobjc-framework-Quartz ; pip install pyobjc-core ; pip install pyobjc
- Linux: pip install python3-xlib; sudo apt-get install scrot python3-tk python3-dev  (Scrot是Pyautogui使用截屏命令需要用到的截屏程序)

最后，当然是记得pip install pyautogui, 安装pyautogui

## 安全机制

在GUI自动化之前，我们要先知道自动化中需要避免的几个问题，电脑执行程序的速度超过我们眼睛所能捕捉的速度，但在日常操作的GUI的过程中，我们不需要那么快的速度，太快的速度反而容易导致程序在操作的过程中产生死机，或是上一个命令的运算成果还没完成，导致下一个步骤失效的问题，如果程序自动化已经在执行，运行的速度又快到让我们无法手动将其停止，这时我们有以下几种方法可以关闭程序避免程序一直执行到死机

1. 通过注销程序: 
    1. Windows: CTRL+ALT+DEL
    2. OS X: Command+Shift+Option+Q
2. 为程序加上Delay或是利用pyautogui中的安全失效异常功能
    1. pyautogui的Delay方法：pyautogui.PAUSE = 2 表示执行完上一个动作以后，等待2秒再进行下一个
    2. pyautogui.FailSafeException : 如果我们往屏幕左上角移动鼠标会触发这个异常，导致程序运行停止；我们可以透过True & False 来开关这个功能
3. 范例程序：

```python
import pyautogui
pyautogui.PAUSE = 2
pyautogui.FAILSAFE = True #开启保护机制
```



## 控制鼠标

pyautogui控制鼠标的函数使用平面坐标 x, y，以左上角为起点，x代表水平递增量，y表示垂直递增量. 如果以1920 x 1080的屏幕分辨率为例，左上角为(0,0), 右下角为(1919, 1079)

### 相关函数

1. pyautogui.size(): 此函数返回两个整数的元组，表示屏幕的分辨率

![](https://raw.githubusercontent.com/xfzlun/xfzlun.github.iogithub/master/%E6%88%AA%E5%B1%8F2020-08-16%20%E4%B8%8B%E5%8D%884.39.45.png)

2. pyautogui.moveTo(): 这个看字面应该猜得到，是移动鼠标用的，没错，我们输入x, y参数就可以指定鼠标移动到我们指定的屏幕位置，另外我们还可以给定第三个参数duration = 整数或是浮点数，表示鼠标移动到指定位置所需要的时间，以秒为单位. (参考范例：mousemoving.py)

![](https://raw.githubusercontent.com/xfzlun/xfzlun.github.iogithub/master/%E6%88%AA%E5%B1%8F2020-08-16%20%E4%B8%8B%E5%8D%884.55.03.png)

3. pyautogui.moveRel(): Rel应该是表示relative吧，所以这个应该指的是相对于鼠标目前位置的相对位置，所以是以鼠标当前位置为起点，移动相对的点数，所以此函数内的位置参数(x,y)就可以包含负整数或是负浮点数，正数表示右移，负数表示左移
4. pyautogui.position(): 确定鼠标当前位置，此函数返回鼠标当前位置的两个参数(x.y)的元组；参见范例程序 whereIsMouseNow.py 
5. 点击鼠标：完整的鼠标点击一下的动作是：按下 --> 放开，在pyautogui库中，按下的函数是mouseDown()，放开鼠标的函数是mouseUp()，相当于释放鼠标按键，但如果要实现点击一下，可以直接使用pyautogui封装好的click()函数。一样传入(x,y)参数，鼠标会在指定位置点击一下，点击一下是click()，想双击就用doubleClick()；click&doubleClick预设都是点击左键，如果需要变动点击的按键，加入第三个参数button = 'right', 'left', 'middle'; 也可以用另外的函数rightClick()或是middleClick()进行右键或是中键的双击
6. Drag: 拖动表示按住鼠标键不放，然后移动位置，这类动作经常在文件处理时出现，pyautogui提供了两个方法，跟前面提到的move一样，分为dragTo()与dragRel()

练习：spiralDraw.py

7. 滚动鼠标 - scroll() ：这边提供一个整数作为参数，代表滚动多少单位，此处的单位跟随不同作业系统有不同定义；另外，正书表示向上滚动，负数表示向下滚动


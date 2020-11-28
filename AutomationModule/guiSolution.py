# -*- coding:utf-8 -*-
'''
安装PysimpleGUI:
$python -m pip install PySimpleGUIQt
'''
import PySimpleGUIQt as sg

#查看所有的主题
#    sg.preview_all_look_and_feel_themes()
#切换主题
sg.change_look_and_feel("GreenMono")

#首先创建一个小部件(widget)
text = sg.Text("This is a test") #建立一个文本部件
textinput = sg.InputText() #建立一个文本输入部件
bt = sg.Button('OK')  #建立一个按钮部件
cbt = sg.Button('Cancel') #建立按钮部件
layout = [[text, textinput],[bt, cbt]]  #建立布局
'''
这里要注意，按行布局要把同一行中的所有部件放入同一个列表，如上面的布局我们就会得到
text, textinput在同一行
bt,与cbt在同一行
最后会形成一个嵌套的列表
'''
#3. 建立窗体，窗体包含名字与我们希望设定的部件
window = sg.Window('Welcome', layout) #输入窗体的名字与我们之前设定好的layout

#4. 创建一个循环让GUI界面运行同时读取与获取输入输出值；一个图形用户交互页面需要一个循环来运行同时等待使用者去做事件
# 一般用一个while循环包含逻辑，break结束
while True:
    event, values = window.read()
    if event in (None, 'Cancel'):
        break
    print(f'Event:{event}')
    print(str(values))
window.close()





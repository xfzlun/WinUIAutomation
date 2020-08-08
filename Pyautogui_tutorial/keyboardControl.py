#键盘控制， 只能输入字符串， 不能输入中文
#输入信息
pg.typewrite(message='test', interval=0.5)

#按住，放开，键盘上的字符
#按住shift
pg.keyDown('shift')
#放开shift
pg.keyUp('shift')

#按一下esc
pg.press('esc')

#组合键
pg.hotkey('ctrl', 'c')

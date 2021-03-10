# 启动3Dmark
'''
import os
os.chdir('c:/Program Files/UL/3DMark')
main = "3DMark.exe"
os.system(main)
'''
import os
os.chdir(r"C:\Program Files\UL\3DMark")  #利用这个方法必须先进入exe执行档所在的位置
main = ".\\3DMark.exe"  #如果不希望阻塞进程，就可以在前面加入start
#r_v = os.system(main)   # 利用这个方法执行，3DMark会出现在任务管理器里面，没法在前台执行
r_v2 = os.popen(main)
#os.system('cd .. && mkdir aaa.txt')
#os.system('cd / ; mkdir aaa.txt')  # os.system 默认阻塞当前程序执行，在 cmd 命令前加入 start 可不阻塞当前程序执行。如下：
#os.system('start ping www.baidu.com -t')
#print(r_v)
print(r_v2)


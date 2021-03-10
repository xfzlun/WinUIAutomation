# 启动3Dmark
'''
import os
os.chdir('c:/Program Files/UL/3DMark')
main = "3DMark.exe"
os.system(main)
'''
import os
current_path = os.getcwd()  #获取当前工作目录
print(current_path)
os.chdir(r"C:\Program Files\UL\3DMark")  #利用这个方法必须先进入exe执行档所在的位置
main = ".\\3DMark.exe"  #如果不希望阻塞进程，就可以在前面加入start, 但这个也是在后台程序里面
#r_v = os.system(main)   # 利用这个方法执行，3DMark会出现在任务管理器里面，没法在前台执行
r_v2 = os.popen(main)
#os.system('cd .. && mkdir aaa.txt')
#os.system('cd / ; mkdir aaa.txt')  # os.system 默认阻塞当前程序执行，在 cmd 命令前加入 start 可不阻塞当前程序执行。如下：
#os.system('start ping www.baidu.com -t')
#print(r_v)
print(r_v2)

'''
import subprocess
#cmd_list = ['cd C:\\Program Files\\UL\\3DMark','3DMark.exe']
subrv = subprocess.Popen('python')
print(subrv)
#subprocess对我们自动化来说，少了变更资料夹的方法，所以在call程式的时候会有困难
'''
'''
import os  
os.chdir("C:\\Program Files\\UL\\3DMark")  #切换目录到3DMark底下，利用这个方法必须先进入exe执行档所在的位置
main = "start 3DMark.exe"
r_v = os.system(main)
print(r_v)
'''


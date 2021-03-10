# python中3种调用可执行文件.exe的方法

# 方法1：os.system()可以保存可执行程序中的打印值和主函数的返回值，且会将执行过程中要打印的内容打印出来
import os
os.chdir("C:\Program Files (x86)\Google\Chrome\Application")  #利用这个方法必须先进入exe执行档所在的位置
main = "chrome.exe"
r_v = os.system(main)
os.system('cd .. && mkdir aaa.txt')
os.system('cd / ; mkdir aaa.txt')  # os.system 默认阻塞当前程序执行，在 cmd 命令前加入 start 可不阻塞当前程序执行。如下：
os.system('start ping www.baidu.com -t')
print(r_v)


# 场景：APP自动化测试，但先启动模拟器
def open_app(app_dir):
    os.startfile(app_dir) #os.startfile（）打开外部应该程序，与windows双击相同
if __name__ == "__main__":
    app_dir = r'G:\yeshen\Nox\bin\Nox.exe'#指定应用程序目录
    open_app(app_dir)

# 方法二、commands.getstatusoutput()  会保存可执行程序中的打印值和主函数的返回值，但不会将执行过程中要打印的内容打印出来
import subprocess  
import os  
main = "project1.exe"
if os.path.exists(main):  
    rc,out= subprocess.getstatusoutput(main)  
    print (rc)
    print ('*'*10)
    print (out)

# 方法三、popen()  会保存可执行程序中的打印值，但不会保存主函数的返回值，也但不会将执行过程中要打印的内容打印出来
import os
main = "project1.exe"
f = os.popen(main)    
data = f.readlines()    
f.close()    
print (data)

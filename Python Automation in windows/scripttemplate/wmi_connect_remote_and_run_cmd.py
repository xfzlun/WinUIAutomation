'''
python 如何远程控制另一台机器-通过cmd执行文件
python 远程控制另一台机器通过cmd执行文件，通过本机控制远程主机执行代码。


————————————————
版权声明：本文为CSDN博主「LaughingSister」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/laughingsister/article/details/104550897
'''

import wmi
import pythoncom
conn = pythoncom.CoInitialize()
def sys_version(ipaddress, user, password):
    conn = wmi.WMI(computer=ipaddress, user=user, password=password)
    for sys in conn.Win32_OperatingSystem():
        print ("Version:%s" % sys.Caption.encode("UTF8"),"Vernum:%s" % sys.BuildNumber) #系统信息
        print (sys.OSArchitecture.encode("UTF8") ) # 系统的位数
        print (sys.NumberOfProcesses) # 系统的进程数
    try:
        filename = r"D:\sc_data\job_agent.bat" # 此文件在远程服务器上
        cmd_callbat = r"cmd /c call %s" % filename
        conn.Win32_Process.Create(CommandLine=cmd_callbat) #执行bat文件 Win32_Process.Create
    except Exception as e:
        print(e)
if __name__ == '__main__':
    sys_version(ipaddress="实际", user="实际", password="实际")

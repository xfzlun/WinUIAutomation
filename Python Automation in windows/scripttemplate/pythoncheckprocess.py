# Python 判断一个进程是否存在

import psutil
 
def judgeprocess(processname):
    pl = psutil.pids()
    for pid in pl:
        if psutil.Process(pid).name() == processname:
            print(pid)
            break
    else:
        print("not found")
        
if judgeprocess('3DMark.exe') == 0:
    print('success')
else:
    pass
# 这个可以检测到，但好像有时候会报错，不知道是不是执行次数太多内存满溢了


# 利用win32com检测进程是否存在

import win32com.client
def check_exist(process_name):
    WMI = win32com.client.GetObject('winmgmts:') 
    print(type(WMI))
    processCodeCov = WMI.ExecQuery('select * from Win32_Process where name="%s"' % process_name)
    if len(processCodeCov) > 0:
        print("%s is exist" % process_name)
    else:
        print("%s is not exist" % process_name)

if __name__ == '__main__':
    check_exist('SearchIndexer.exe')

'''
用这个方法扫描不到后台的进程，
只能看到部分信息，不是所有的进程都在这个Win32_Process里面，貌似只有系统的进程在
'''
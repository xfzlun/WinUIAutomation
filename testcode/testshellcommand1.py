#coding=utf-8
 
import win32api
#日报软件启动
win32api.ShellExecute(0, 'open', r'C:\Program Files\UL\3DMark\3DMark.exe', '','',1)
 
#OA启动
#win32api.ShellExecute(0, 'open', r'C:\Program Files\Tongda\ispirit\ispiritPro.exe', '','',1)
 
#QQ启动
#win32api.ShellExecute(0, 'open', r'D:\QQ\Bin\QQ.exe', '','',1)
 
#......
#当然你还可以添加很多你需要启动的软件


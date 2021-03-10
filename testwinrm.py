import winrm
wintest = winrm.Session('http://192.168.0.110:5985/wsman',auth=('Luntest','qtc12345'))
#chdirecotry = wintest.run_cmd('cd C:\\Program Files\\UL\\3DMark \r&' '3DMark')
#run3D = wintest.run_ps('Start-Process C:\\Program FIles\\UL\\3DMark\\3DMark.exe')


#run3D = chdirecotry.run_cmd('3DMark.exe')
#run3D = wintest.run_cmd('python "F:\\AutomationWinTest\\Python Automation in windows\\scripttemplate\\runfile.py"')  # 这也是在后台运行
print(run3D)

# code = ret.status_code





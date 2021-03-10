#!/usr/ftpbin/env python
# -*- encoding: utf-8 -*-
'''
@version :   0.0.1
@File    :   RemoteWIn.py
@Time    :   2019/07/04 15:07:13
@Author  :   KANGXINWEN 
@Software:   PyCharm
@Version :   1.0
@Author_email : singbogo@163.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA
@Desc    :   
#    远程管理window
  1、A安装模块 pip install pywinrm
  2、B配置winrm服务的相关配置
    winrm service 的基础配置，执行之后提示选择的时候选中y：
    winrm quickconfig
    查看winrm service listener（分为http和https）:
    winrm e winrm/config/listener
    为winrm service 配置auth:
    winrm set winrm/config/service/auth @{Basic="true"}
    为winrm service 配置加密方式为允许非加密：
    winrm set winrm/config/service @{AllowUnencrypted="true"}
    查看winrm服务的配置：
    winrm get winrm/config
  3、测试
    import winrm
    wintest = winrm.Session('http://B主机的ip地址:5985/wsman',auth=('administrator','abc123!'))
    ret = wintest.run_cmd('ipconfig')
    print(ret)
  4、简单的一些系统命令能够执行， 但是当一个命令在一直执行，Pywinrm的会进行一直等待，不便于观察命令的执行
'''
 
# here put the import ftplib
import winrm
import sys
#from util.logutil.log import loginfo  # 这个是博主自己写的内置库，可以用printf取代
 
 
class AutomainPlantfRomteWin(object):
    
    def __init__(self, *args):
        self.host, self.port, self.author = args[0][0], args[0][1], args[0][2]
        self._session = self.session1(self.host, self.port, self.author)
 
    def isconnected(self):
        """ is Connection successful """
        if self._session is None:
            return False
        else:
            return True
 
    def session1(self, *args):
        """ 创建远程session 
        @args: 
                arg0+arg1: host+port  http://+host+port+/wsman http://127.0.0.1:5985/wsman
                arg2: auth  (username, passwd)
        """
        # 当args的长度不为3
        if len(args) != 3:
            return
        host = "http://" + str(args[0]) + ":" + str(args[1]) + "/wsman"
        print(host)
        return winrm.Session(host, auth=args[2])
 
    def close(self):
        """ 关闭会话 """
        if self._session:
            pass
            # self._session
 
    def run_ps(self, script):
        """
        运行脚本
        :param script:
        :return:
        """
        if script is None:
            return
        loginfo("run Script %s"%script)
        response = self._session.run_ps(script)
        self.dispose(response)
 
    def send(self, command):
        """ 远程执行命令 返回是对象 获取返回的Text： result.std_out """
        if self._session is None:
            return None
        loginfo("run command %s"%command)
        status = self._session.run_cmd(command)
        return status
 
    def always_perform(self):
        """ 模式： 创建session 等待屏幕输入  发送远程命令  接受结果  等待命令 如果是 'quit', 'bye', 'exit', <ctrl + x> 退出并关闭session"""
        prompt = '\ntell me something, and I will repeat it back to you:'
        prompt += "\nEnter 'quit' or 'bye' or 'exit' to end the program.\n"
        sys.stdout.write(prompt)
 
        response, message = str(), str()
        while message not in ('quit', 'bye', 'exit'):
            message = input('>>>')
            if message not in ('quit', 'bye', 'exit'):
                # 发送远程命令
                response = self.send(message)
                # 处理返回信息
                self.dispose(response)
            else:
                # self.close()
                break
 
    def dispose(self, object):
        """ 处理信息 返回状态判断 字符类型转换 格式化输出 """
        if object is None:
            return False
        message = str()
        bstatus = bool(False)      # Returns whether the command was executed successfully. default: False
        # status_code 成功为0  失败为1
        # sometime status_code is 0 but return msg is in std_err
        if object.status_code is 0:
            message = object.std_out
            # std_out is 0, get msg from std_err
            if len(message) is 0 or message is "":
                message = object.std_err
                bstatus = False
            else:
                bstatus = True
        else:
            message = object.std_err
            bstatus = False
        try:
            message = message.decode('utf-8')
        except:
            message = message.decode('gbk') 
        print(message)
        return bstatus
 
    def upload(self, filename, romterpath):
        """
        dos command net share:
            0、net share查看开启的共享
            net use \\127.0.0.1\ipc$ singebogo /user:KANGXINWEN    连接目标机的ipc$建立空连接 # net use h: \\ip\c$ "密码" /user:"用户名" 直接登陆后映射对方C：到本地为H:
            xcopy E:\backup.txt \\192.168.1.249\D$\vim /D /Y /K  使用xcopy上传本地E盘下backup.txt文件至目标服务器D盘下vim文件夹
                /D:m-d-y     复制在指定日期或指定日期以后更改的文件。 如果没有提供日期，只复制那些源时间比目标时间新的文件。
                /Y           取消提示以确认要覆盖现有目标文件。
                /K           复制属性。一般的 Xcopy 会重设只读属性。
            net use \\192.168.1.249\ipc$ /delete
        :return:
        """
        # 显示远程主机的共享资源列表
        netview = """net share"""
        self.dispose(self.send(netview))
        # Exist then delete C$
        detele_netuser = "net share C$ /delete"
        print(self.dispose(self.send(detele_netuser)))
        # open IPC$
        netshareIPC = "net share ipc$"
        self.dispose(self.send(netshareIPC))
        # remoter drive specification C map to localtor h
        netuser = "net use h: \\\\%s\c$ %s /user:%s"%(self.host, self.author[1], self.author[0])
        print(self.dispose(self.send(netuser)))
 
        # copy localtor file to map specification
        xcopy = "xcopy %s %s"%(filename, romterpath)
        print(self.dispose(self.send(xcopy)))
        # delete map specification
        detele_netuser = "net use \\\\%s\c$ /delete"%self.host
        print(self.dispose(self.send(detele_netuser)))
        return netshareIPC, netuser, xcopy, detele_netuser
 
 
if __name__ == "__main__":
    list1 = ("192.168.0.110", "5985", ('Luntest','qtc12345'))
    remotewin = AutomainPlantfRomteWin(list1)
    if remotewin.isconnected() is True:
        # remotewin.dispose(remotewin.send("java -Dwebdriver.ie.driver=F:\document\Source\AutoMation\python\AutoMation_Frame\AutomainPlatformUI\drivers\IEDriverServer.exe -jar F:\document\Source\AutoMation\python\AutoMation_Frame\AutomainPlatformUI\drivers\selenium-server-standalone-3.141.59.jar -role node -hub http://ip:4445/grid/register"))
        # remotewin.dispose(remotewin.send("java -jar F:\document\Source\AutoMation\python\AutoMation_Frame\AutomainPlatformUI\drivers\selenium-server-standalone-3.141.59.jar -role hub -port 4446"))
        remotewin.always_perform()
        # print(remotewin.upload("F:\\\\document\\\\IODemo1.java", "h:\\"))
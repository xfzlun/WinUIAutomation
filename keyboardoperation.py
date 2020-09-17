'''
这支工具主要提供测试中需要操作keyboard的功能
思路：
设计一个类，加入
1. keycode转码方法，
2. ssh命令
'''


#ssh远程命令
import paramiko

ssh = paramiko.SSHClient()
key = paramiko.AutoAddPolicy()
ssh.set_missing_host_key_policy(key)
ssh.connect('127.0.0.1', 22, 'user', 'passwd' ,timeout=5)
stdin, stdout, stderr = ssh.exec_command('ls -l')

for i in stdout.readlines():
    print(i)
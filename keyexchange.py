
'''
根据输入的参数，转成对应的keycode
1. 输入键盘按键
2. 查找hid_key_value.txt
3. 匹配对应的字母或是单词
4， 切分对应的字符串
5. 用with open
'''
import paramiko
import time

'''
class
新建一个电脑操作类，初始化参数加入ip地址，账号密码
'''
with open("WInAutomation/hid_key_value.txt", "r") as fp: # 打开keycode value文件
    lines = fp.readlines()   # 逐行读取档案内容
    dict = {}  # 创造一个空字典，准备存入读取的数据
    for line in lines: #遍历lines内的内容
        line = line.strip('\n') #去除换行符
        ddict = line.split('<-->') # 将读取出来的字符串，用split根据'<-->'切分后返回给ddict，此为一个列表
        dict[ddict[1]] = ddict[0]  # 向字典中新增一个键：值
print(dict)
'''
def alphaNumExchange(strings):  # 定义一个函数做keycode转换
这里有一个问题，当输入字串的时候，我需要判断目前输入的是字符串，所以我需要拆成单个字母，但如果是function key,我就需要判断是functionkey
先写成2个函数吧....
完美的实现方式应该是一个函数，可以接收3种函数，字符串，单一功能键，组合键...
'''
'''
    alpha = list(strings)  # 用list方法把输入的字符串拆成一个个英文字母
    print(alpha)
    print(type(alpha))
    keycode = []  # 定义一个空列表，预计装入分解后的keycode
    for i in alpha: # 遍历char
        keycode.append(dict[i])  # 根据字母当作键，从字典中取出对应键的值加入keycode列表
        #print(keycode)
    #keycode = dict[string]
    return keycode

def funcKeyExchange(functionkey):
    funckeycode = dict[functionkey]
    return funckeycode
'''

def alphaNumExchange(strings, function):  # 定义一个函数做keycode转换
    keycode = []
    if strings != None:
        alpha = list(strings)  # 用list方法把输入的字符串拆成一个个英文字母
        print(alpha)
        print(type(alpha))
        #keycode = []  # 定义一个空列表，预计装入分解后的keycode
        for i in alpha: # 遍历char
            keycode.append(dict[i])  # 根据字母当作键，从字典中取出对应键的值加入keycode列表
            #print(keycode)
        #keycode = dict[string]
        #return keycode
    else:
        pass
    if function != None:
        keycode.append(dict[function])
        #return keycode
    else:
        pass
    return keycode
    print(keycode)


    

def funcKeyExchange(functionkey):
    funckeycode = dict[functionkey]

#ssh远程命令
'''
另一种写法
def Sshcommand(funckeycode:str, *keycodes):
'''
def Sshcommand(keycodes):
    ssh = paramiko.SSHClient()
    key = paramiko.AutoAddPolicy()
    ssh.set_missing_host_key_policy(key)
    ssh.connect('10.46.202.132', 22, 'root', 'ch7eng9' ,timeout=15)   #要执行shell command需要root远程登入
    print(type(keycodes))
    if keycodes == None:
        pass
    else:
        for i in keycodes:
            shellCommand = 'echo -ne "%s" > /dev/hidg0' % i
            stopKeyin = 'echo -ne "\\0\\0\\0\\0\\0\\0\\0\\0" > /dev/hidg0'  
            print(shellCommand)
            stdin, stdout, stderr = ssh.exec_command(shellCommand)
            time.sleep(0.2)
            stdin, stdout, stderr = ssh.exec_command(stopKeyin)
            #print(stdout)
            time.sleep(0.5)
    #




a = alphaNumExchange(None, "F1")
#b = funcKeyExchange("PrintScreen")
#print(b)
print(a)
#print(type(a))

Sshcommand(a)





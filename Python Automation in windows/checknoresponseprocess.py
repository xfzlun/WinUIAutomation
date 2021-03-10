'''
python练手脚本-定时检测无响应进程并重启

零壹视界 2019-04-21 21:59:52  625  收藏 1
分类专栏： 有用的轮子
版权
背景
总有一些程序在windows平台表现不稳定，动不动一段时间就无响应，但又不得不用，每次都是发现问题了手动重启，现在写个脚本定时检测进程是否正常，自动重启。

涉及知识点
schedule定时任务调度

os.popen运行程序并读取解析运行结果
————————————————
版权声明：本文为CSDN博主「零壹视界」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
原文链接：https://blog.csdn.net/u011606307/article/details/89440681
'''


import os
import time

import schedule


def parse_output(output):   # 解析命令执行结果
    print(output)
    pid_list = []
    lines = output.strip().split("\n")
    if len(lines) > 2:
        for line in lines[2:]:
            pid_list.append(line.split()[1])
    return pid_list


def list_not_response(process_name):  # 查找符合条件的进程列表
    return list_process(process_name, True)


def list_process(process_name, not_respond=False):   # 查找符合条件的进程列表
    cmd = 'tasklist /FI "IMAGENAME eq %s"'
    if not_respond:
        cmd = cmd + ' /FI "STATUS eq Not Responding"'
    output = os.popen(cmd % process_name)
    return parse_output(output.read())


def start_program(program):
    os.popen(program)


def check_job():   # 检查无响应进程并重启
    process_name = "xx.exe"
    not_respond_list = list_not_response(process_name)
    if len(not_respond_list) <= 0:
        return
    pid_params = " ".join(["/PID " + pid for pid in not_respond_list])
    os.popen("taskkill /F " + pid_params)
    if len(list_process(process_name)) <= 0:
        start_program(r'E:\xxx\xx.exe')


if __name__ == '__main__':   #脚本主入口
    schedule.every(5).seconds.do(check_job)
    while True:
        schedule.run_pending()
        time.sleep(1)

'''
# schedule的其它示例

import schedule
import time

def job(message='stuff'):
    print("I'm working on:", message)

#每10分钟
schedule.every(10).minutes.do(job)
#每小时
schedule.every().hour.do(job, message='things')
#每天10点30分
schedule.every().day.at("10:30").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
'''

'''
python3，windows下的进程监控脚本
1  安装psutil，pip install psutil、

2  查看进程id，可通过任务管理器查看

3  cmd下进入脚本所在路径

4  执行脚本（python monitor.py 30658）

5 脚本所在路径下，生成监控日志文件
'''

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#@Time      : 2018/12/12 9:58
#@Author    : lmh
#@File      : monitor.py      
#
#
import sys
import psutil
import datetime
import time
 
 
def monitor(pid):
    # 设定监控时间  默认3天
    CYCLE_TIME = datetime.timedelta(weeks=0, days=3, hours=00, minutes=0, seconds=5, microseconds=0,
                                    milliseconds=0)  # 60*60*24
    start_time = datetime.datetime.today()
    # 判断进程是否存在
    if (psutil.pid_exists(pid)):
        p = psutil.Process(pid)  # 实例化一个进程
        pName = p.name()  # 进程名
        # 设置日志名
        logName = pName + "_" + str(pid) + "_stress_monitoring_record.log"  # log文件
        logfile = open(logName, "a")
    else:
        print("pid is not exists please enter true pid!!!")
        return
    wTime = 30  # 等待时间
 
    while (True):
        # 判定监控时间
        if ((datetime.datetime.today() - start_time) > CYCLE_TIME):
            break
 
        recTime = time.strftime('%Y-%m-%d\t%H:%M:%S', time.localtime(time.time()))  # datetime.datetime.today() #记录时间
 
        # 判断进程是否存在
        if (psutil.pid_exists(pid)):
            vmm = p.memory_info().vms  # 虚存 单位字节
            mm = p.memory_info().rss  # 实际使用内存 单位字节
            pCpu = p.cpu_percent(interval=1)  # CPU百分比
            nFiles = len(p.open_files())  # 打开文件数   这个不太准感觉，暂不记录
            nThreads = p.num_threads()  # 线程数
            nHandles = p.num_handles()  # 句柄数
            # 记录进程详细信息
            monitor_content = str(recTime) + "\t" + str(vmm) + "\t" + str(mm) + "\t" + str(pCpu) + "\t" + str(
                nThreads) + "\t" + str(nHandles) + "\n"
 
        else:
            monitor_content = str(datetime.datetime.today()) + "\t" + str(pid) + "  is not running!!!!!!!!!\n"
            break
 
        print(monitor_content)
        logfile.flush()
        logfile.write(monitor_content)  # 写入log文件
        time.sleep(wTime)  # 循环等待
 
    logfile.close()
 
 
if __name__ == "__main__":
    # 主函数
    if len(sys.argv) < 2:
        print("usage: python monitor.py 进程id")
        sys.exit()
    pid_str = sys.argv[1]
    pid = int(pid_str)
    monitor(pid)
    pass
# windows进程监控

#!/usr/bin/python
# _*_ coding: UTF-8 _*_
# Filename : watchProcess.py
#author by :morespeech
#python2.7
#platform:pycharm,windows
#topic: practice every day
#detial: watch process
 
 
import platform
import os
import win32ui, win32api, win32con, win32gui
import subprocess
import psutil
import time
from datetime import date, datetime, timedelta
 
class cTime:
    def __init__(self, day, hour, min, second):
        self.day = day
        self.hour = hour
        self.minute = min
        self.second = second
 
class cTerminateThresh:
    def __init__(self, maxThreadNum, maxOpenFilesNum, maxRamUsage, maxCpuUsage):
        self.__maxThreadNum = maxThreadNum
        self.__maxOpenFilesNum = maxOpenFilesNum
        self.__maxRamUsage = maxRamUsage
        self.__maxCpuUsage = maxCpuUsage
 
    def GetMaxThreadNum(self):
        return self.__maxThreadNum
 
    def GetMaxOpenFilesNum(self):
        return self.__maxOpenFilesNum
 
    def GetMaxRamUsage(self):
        return self.__maxRamUsage
 
    def GetMaxCpuUsage(self):
        return self.__maxCpuUsage
 
 
class cWatchProcess:
    def __init__(self, processname, updatetime, terminatethresh):
        self.processName = processname
        self.updataTime = updatetime
        self.Process = ''
        self.teminatethresh = terminatethresh
 
    ##public interface#
    def getProcessInfo(self):
        # Init time
        starttime = datetime.now()
 
        # parse step time
        period = timedelta(days=updatetime.day, hours=updatetime.hour, minutes=updatetime.minute, seconds=updatetime.second)
        endtime = starttime + period
        endtimestr = endtime.strftime('%Y-%m-%d %H:%M:%S')
        count = 0
        while True:
            time.sleep(0.5)   #save cpu
            # Get current time
            starttime = datetime.now()
            starttimestr = starttime.strftime('%Y-%m-%d %H:%M:%S')
            if str(starttimestr) == str(endtimestr):
                endtime = starttime + period
                endtimestr = self.__displaytTime(endtime, count, " get info time:")
                count += 1
                try:
                    self.Process = self.__getProcByName()
                except Exception, e:
                    print Exception, ":", e
 
                if self.Process != None:
                    print "process name is: %s" % self.Process.name()
                    print("pid is (%s)" % self.Process.pid)
 
                    if not (self.__checkCpu() and self.__checkRam() and self.__checkOpenFileNum() \
                            and self.__checkThreadNum()):
                        continue
 
                else:
                    print "can't find the process : %s" % self.processName;
                continue
 
#private
    def terminateProcess(self, log):
        print log
        self.Process.terminate()
        self.Process.wait(timeout=5)
 
    def __checkCpu(self):
        cpuUsage = self.Process.cpu_percent(interval=1)
        print("cpu percent is (%s)" % cpuUsage)
        if (self.teminatethresh.GetMaxCpuUsage() - cpuUsage) < 0.1:
            self.terminateProcess("cpu percent exceed thresh, and this process will be terminated!")
            return 0
        return 1
 
    def __checkRam(self):
        ramInfo = self.Process.memory_info()
        print "memory size is (%d)Bytes" % ramInfo.rss
        ramPercent = self.Process.memory_percent()
        print("memory percent is (%s)" % ramPercent)
        if (self.teminatethresh.GetMaxRamUsage() - ramPercent) < 0.1:
            self.terminateProcess("memory percent exceed thresh, and this process will be terminated !")
            return 0
        return 1
 
    def __checkThreadNum(self):
        threadsNum = self.Process.num_threads()
        print("threads number is (%s)" % threadsNum)
        if (threadsNum > self.teminatethresh.GetMaxThreadNum()):
            self.terminateProcess("threads number exceed thresh, and this process will be terminated !")
            return 0
        return 1
 
    def __checkOpenFileNum(self):
        allFiles = list(self.Process.open_files())
        print("open files size is (%d)" % len(allFiles))
        if (len(allFiles) > self.teminatethresh.GetMaxOpenFilesNum()):
            self.terminateProcess("open files number exceed thresh, and this process will be terminated!")
            return 0
        return 1
 
 
    def __getProcById(pid):
        return psutil.Process(pid)
 
 
    #get process by name, return the first process if there are more than one
    def __getProcByName(self):
        for proc in psutil.process_iter():
            try:
                if proc.name().lower() == self.processName.lower():
                    return proc
            except psutil.AccessDenied:
                pass
            except psutil.NoSuchProcess:
                pass
        return None
 
    def __displaytTime(self, cur, count, log):
        strcur = cur.strftime('%Y-%m-%d %H:%M:%S')
        print count, log, strcur
        return strcur
 
 
g_processname=''
g_updatetime=10   #second
 
def parse():
    from optparse import OptionParser
    usage = "usage:watchProcess [opthions] -p QQ.exe -t 10"
    parser = OptionParser(usage=usage)
    parser.add_option("-p", "--processname", dest = "wantprocessName",help="process name that you want to watch, QQ.exe etc")
    parser.add_option("-t", "--time", dest = "wantupdateTime", help="updata results every n seconds ")
    (options, args) = parser.parse_args()
 
    if options.wantprocessName and options.wantupdateTime:
        global g_processname, g_wantupdatetime
        g_processname = options.wantprocessName
        g_updatetime = options.wantupdateTime
    else:
         parser.print_help()
 
 
if __name__ == '__main__':
    parse()
    terminatethresh = cTerminateThresh(10, 200, 60, 60)    #set the thresh. if the process takes up too much resources, which will be te terminated.
    updatetime = cTime(0, 0 , 0, g_updatetime)              #get process info every other updatetime
    cWatchProcess(g_processname, updatetime, terminatethresh ).getProcessInfo()
 
 
 
 
 
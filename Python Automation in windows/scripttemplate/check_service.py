
from win32com.client import GetObject
import wmi,sys,argparse,subprocess

parser = argparse.ArgumentParser( usage = 'check_win_service.py -t xx -n xxxx -cw xx.xx -cc xx.xx -mw xx.xx -mc xx.xx', description='to check windows iis thrift or process usages' )
parser.add_argument( '-t', dest='type', metavar='string', type=str, required=True, help='resource type:iis|srv|app' )
parser.add_argument( '-n', dest='name', metavar='string', type=str, required=True, help='service or app name' )
parser.add_argument( '-cw', dest='cpuwarn', metavar='float', type=float, nargs='?', const=80.00, help='warning value for cpu,default 80%' )
parser.add_argument( '-cc', dest='cpucrit', metavar='float', type=float, nargs='?', const=90.00, help='critial value for cpu,default 90%' )
parser.add_argument( '-mw', dest='memwarn', metavar='float', type=float, nargs='?', const=15.00, help='warning value for mem,default 15%' )
parser.add_argument( '-mc', dest='memcrit', metavar='float', type=float, nargs='?', const=20.00, help='critial value for mem,default 20%' )
parser.add_argument( '-tw', dest='tcpwarn', metavar='int', type=int, nargs='?', const=800, help='warning value for tcp,default 800' )
parser.add_argument( '-tc', dest='tcpcrit', metavar='int', type=int, nargs='?', const=1000, help='critial value for tcp,default 1000' )
args = parser.parse_args()


def iis_usage(iisname):
    wmi = GetObject('winmgmts:/root/cimv2')
    iisbase = wmi.ExecQuery('select * from Win32_PerfFormattedData_W3SVCW3WPCounterProvider_W3SVCW3WP where Name like "%{}"'.format(iisname))

    for item in iisbase:
        iispid = item.Name.split('_')[0]

    iisstatus = []

    try:
        iisinfo = wmi.ExecQuery('select * from Win32_PerfFormattedData_PerfProc_Process where IDProcess = "{}"'.format(iispid))
    except UnboundLocalError as nopid:
        print("CRITIAL - {} was down".format(iisname))
        sys.exit(2)

    for item in iisinfo:
        iisstatus.append(item.PercentProcessorTime)
        iisstatus.append(round(float(item.WorkingSetPrivate)/1024/1024,2))
    iiscon = wmi.ExecQuery('select * from Win32_PerfFormattedData_W3SVC_WebService where Name = "{}"'.format(iisname))
    for item in iiscon:
        iisstatus.append(item.CurrentConnections)

    return(iisname,iispid,iisstatus)	

	
def srv_usage(srvname):
    wmi = GetObject('winmgmts:/root/cimv2')
    srvbase = wmi.ExecQuery('select * from Win32_Service where Name = "{}"'.format(srvname))

    for item in srvbase:
        srvpid = item.ProcessId

    srvstatus = []

    try:
        srvinfo = wmi.ExecQuery('select * from Win32_PerfFormattedData_PerfProc_Process where IDProcess = "{}"'.format(srvpid))
    except UnboundLocalError as nopid:
        print("CRITIAL - {} was down".format(srvname))
        sys.exit(2)

    for item in srvinfo:
        srvstatus.append(item.PercentProcessorTime)
        srvstatus.append(round(float(item.WorkingSetPrivate)/1024/1024,2))
    srvstatus.append(subprocess.getstatusoutput('netstat -ano | findstr {} | wc -l'.format(srvpid))[1])
    
    return(srvname,srvpid,srvstatus)

def app_usage(appname):
    wmi = GetObject('winmgmts:/root/cimv2')
    appbase = wmi.ExecQuery('select * from Win32_Process where CommandLine like "%{}%" and Caption != "python.exe"'.format(appname))
    for item in appbase:
        apppid = item.ProcessId

    appstatus = []

    try:
        appinfo = wmi.ExecQuery('select * from Win32_PerfFormattedData_PerfProc_Process where IDProcess = "{}"'.format(apppid))
    except UnboundLocalError as nopid:
        print("CRITIAL - {} was down".format(appname))
        sys.exit(2)

    for item in appinfo:
        appstatus.append(item.PercentProcessorTime)
        appstatus.append(round(float(item.WorkingSetPrivate)/1024/1024,2))
    appstatus.append(subprocess.getstatusoutput('netstat -ano | findstr {} | wc -l'.format(apppid))[1])
    
    return(appname,apppid,appstatus)
	
def judgement(judgetype,judgename,judgecpuw,judgecpuc,judgememw,judgememc,judgeconw,judgeconc):
    wmi = GetObject('winmgmts:/root/cimv2')
    totalmem = wmi.ExecQuery('select * from Win32_PhysicalMemory')
    memtotal = 0
    for item in totalmem:
        memtotal += round((float(item.Capacity)/1024)/1024,2)
    
    if judgetype == 'iis':
        stu = iis_usage(args.name)
    elif judgetype == 'srv':
        stu = srv_usage(args.name)
    elif judgetype == 'app':
        stu = app_usage(args.name)
    else:
        print("there have not this type")
        sys.exit(3)

    statstr = "OK"
    status = 0
    cp = float(stu[2][0])
    mp = round((float(stu[2][1])/memtotal)*100, 2)
    tp = int(stu[2][2])
    if cp < judgecpuw and mp < judgememw and tp < judgeconw:
        pass
    elif judgecpuw <= cp < judgecpuc or judgememw <= mp < judgememc or judgeconw <= tp < judgeconc:
        status = 1
        statstr = "WARNING"
    elif judgecpuc <= cp[3][0] or judgememc <= mp or judgeconc <= tp:
        status = 2
        statstr = "CRITIAL"
    else:
        status = 3
        statstr = "UNKNOWN"
    print("{0} - {1} PID:{2}, Cpu Usage:{3}%,Mem Usage:{4}% {5}MB,Tcp Sockes:{6}CON | Cpu={3}%;{7};{8} Mem={4}%;{9};{10} MemUsage={5}MB;; Tcp={6}CON;{11};{12}"
          .format(statstr,stu[0],stu[1],cp,mp,stu[2][1],tp,judgecpuw,judgecpuc,judgememw,judgememc,judgeconw,judgeconc))
    sys.exit(status)


judgement(args.type,args.name,args.cpuwarn,args.cpucrit,args.memwarn,args.memcrit,args.tcpwarn,args.tcpcrit)
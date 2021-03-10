from win32com.client import GetObject
import wmi,sys,argparse

parser = argparse.ArgumentParser( usage = 'check_win_network.py -w xx.xx -c xx.xx', description='to check linuxs mem or net usages' )
parser.add_argument( '-t', dest='type', metavar='string', type=str, required=True, help='resource type:mem|net' )
parser.add_argument( '-d', dest='devs', metavar='string', type=str, nargs='?', const="eth0", help='network card name,do not define it if type is not "net"' )
parser.add_argument( '-w', dest='warn', metavar='float', type=float, nargs='?', const=80.0, help='warning value,default 80' )
parser.add_argument( '-c', dest='crit', metavar='float', type=float, nargs='?', const=90.0, help='critial value,default 90' )
args = parser.parse_args()


def net_usage(dev="eth0", warning=80.00, critical=90.00):
    wmi = GetObject('winmgmts:/root/cimv2')
    networks = wmi.ExecQuery('select * from Win32_PerfFormattedData_Tcpip_NetworkInterface')
    netinfo=[]
    for item in networks:
        if item.Name == dev:
            netinfo.append(item.Name)
            netinfo.append(round(float(item.BytesReceivedPersec)*8/1024/1024,2))
            netinfo.append(round(float(item.BytesSentPersec)*8/1024/1024,2))
            netinfo.append(round(float(item.BytesTotalPersec)*8/1024/1024,2))
            netinfo.append(round(float(item.CurrentBandwidth)/1000/1000,0))
            netinfo.append(item.PacketsReceivedPersec)
            netinfo.append(item.PacketsSentPersec)
            netinfo.append(item.PacketsPersec)

    exitflag = 0
    status="OK"

    warning_line = netinfo[4] * (warning/100)
    critical_line = netinfo[4] * (critical/100)
    usepec = round((netinfo[3] / netinfo[4]) * 100,2)
    tp = netinfo[3]
    if tp < warning_line:
        pass
    elif warning_line <= tp < critical_line:
        exitflag = 1
        status="WARNING"
    elif tp >= critical_line:
        exitflag = 2
        status="CRITICAL"
    else:
        print("UNKNOW")
        sys.exit(3)

    print("{0} - {1} NetWork Usage: Network wide {2}Mbps, Use_Persent {3}%, Total_RX-TX {4}Mbps, RX {5}Mbps ,RX-package {6}, TX {7}Mbps, TX-package {8} | Use_Persent={3}%;;; Total_RX-TX={4}Mbps;{9};{10}; RX={5}Mbps;;; RX-package={6};;; TX={7}Mbps;;; TX-package={8};;;"
          .format(status,netinfo[0],netinfo[4],usepec,netinfo[3],netinfo[1],netinfo[5],netinfo[2],netinfo[6],warning_line,critical_line))
    sys.exit(exitflag)


def mem_usage(warning=80.00, critical=90.00):
    wmi = GetObject('winmgmts:/root/cimv2')
    totalmem = wmi.ExecQuery('select * from Win32_PhysicalMemory')
    freemem = wmi.ExecQuery('select * from Win32_PerfFormattedData_PerfOS_Memory')
    
    memtotal = 0.0
    memused = 0.0
    memfree = 0.0
    memcache = 0.0
    
    for item in totalmem:
        memtotal += round((float(item.Capacity)/1024)/1024,2)
    for item in freemem:
        memfree = float(item.AvailableMBytes)
        memcache = round(float(item.CacheBytes)/1024/1024,2)
        memused = memtotal - memfree

    exitflag = 0
    status="OK"
    warning_mem = round((warning/100) * memtotal,2)
    critical_mem = round((critical/100) * memtotal,2)
    
    if memused < warning_mem:
        pass
    elif warning_mem <= memused < critical_mem:
        exitflag = 1
        status="WARNING"
    elif memused >= critical_mem:
        exitflag = 2
        status="CRITICAL"
    else:
        print("UNKNOW")
        sys.exit(3)

    print("{0} - Mem Usage: Use_Persent {1}%, total {2}MB, free {3}MB, used {4}MB, cache-buffer {5}MB | Use_Persent={1}%;;; total={2}MB;;; free={3}MB;;; used={4}MB;{6};{7}; cache-buffer={5}MB;;;"
          .format(status,round((memused/memtotal)*100,2),memtotal,memfree,memused,memcache,warning_mem,critical_mem))
    sys.exit(exitflag)


    

if args.type == "mem":
    mem_usage(args.warn, args.crit)
elif args.type == "net":
    net_usage(args.devs,args.warn,args.crit)
else:
    print(args.type)
    print("no this types -h for help")
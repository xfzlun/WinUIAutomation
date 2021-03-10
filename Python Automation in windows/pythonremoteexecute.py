# python远程执行命令

import paramiko
def sshclient_execmd(hostname, port, username, password, execmd):
    paramiko.util.log_to_file("paramiko.log")
    s = paramiko.SSHClient()
    s.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    s.connect(hostname=hostname, port=port, username=username, password=password)
    stdin, stdout, stderr = s.exec_command (execmd)
    stdin.write("Y")
    print stdout.read()
    s.close()
def main():
    hostname = '192.168.56.11'
    port = 22
    username = 'root'
    password = '123456'
    execmd1 = "/root/tomcat/bin/stop.sh"
    execmd2 = "/root/tomcat/bin/start.sh"
    sshclient_execmd(hostname, port, username, password, execmd1)
    sshclient_execmd(hostname, port, username, password, execmd2)
if __name__ == "__main__":
    main()
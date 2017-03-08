#!/usr/bin/python3
# -*-coding:utf-8 -* 

import os
import subprocess
import psutil
import signal
import pwd
import time
import sys
import select
import tty
import termios
import getpass

def get_pname(id):#{
    p = subprocess.Popen(["ps -o comm= {}".format(id)], stdout=subprocess.PIPE, shell=True)
    return str(p.communicate()[0])
        #}

def refresh(pid):
    while True:
        stats = {}
        stats['pid'] = psutil.Process(pid)
        stats['Cpu'] = stats['pid'].cpu_percent(interval = 1)
        stats['Memory'] = round(stats['pid'].memory_percent(), 1)
        stats['parentId'] = psutil.Process(pid).ppid()
        stats['Username'] = stats['pid'].username()
        stats['Cmdline'] = get_pname(pid).rstrip('\n')
        stats['Status'] = stats['pid'].status()
        return stats
    
def get_process():#{
    tab = []
    dict = {}
    dirs = os.listdir("/proc")
    for pid in dirs:#{
        if pid.isdigit():#{
            name = get_pname(pid)
            dict["pid"] = pid.strip()
            dict["name"] = name.strip()
            tab.append(dict)
            dict = {}
        #}
    #}
    return (tab)
#}

def kill_process():#{
    os.system('setterm -term linux -back blue -fore white')
    os.system('clear')
    dirs = os.listdir("/proc")
    for pid in dirs:#{
    	try:#{
            pidDel = input("PID of the process to kill : ")
            try:
                if psutil.pid_exists(pidDel):#{
                    try:#{
                        name = get_pname(pidDel)
                        p = psutil.Process(pidDel)
                        p.terminate()
                        print "Succesful kill of :", name.rstrip('\n'), ", Added to syslog.txt"
                        fn = os.path.abspath("log/syslog.txt")
                        print fn
                        syslog = open(fn, "a")
                        syslog.write("Kill of : ")
                        syslog.write(name.rstrip('\n'))
                        syslog.write("\n")
                        syslog.close()
                        return (0)
                #}
                    except psutil.AccessDenied:
                        print "You don't have the right to kill the process :", name.rstrip('\n')
                        return (0)
            #}
                else:
                    print "No process found with the pid \"{}\".".format(pidDel)
                    return (0)
            except OverflowError:
                print "No process found with the pid \"{}\".".format(pidDel)
                return (0)
        except (NameError, TypeError, SyntaxError):
            print "The input need a valid integer, the Pid of a process."
            return (0)
        #}
    #}
    os.system('setterm -term linux -back black -fore white')
    return (0)
#}

def isData():
    return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

def statuts_process():#{
    os.system('setterm -term linux -back blue -fore white')
    os.system('clear')
    try:#{
        pidStat = input("PID of the process you want to get more details : ")
        os.system('clear')
        try:
            if psutil.pid_exists(pidStat):#{
                old_settings = termios.tcgetattr(sys.stdin)
                try:#{
                    tty.setcbreak(sys.stdin.fileno())
                    while 42:
                        try:#{
                            stats = refresh(pidStat)
                            print "PPID :", stats['parentId']
                            print "PID :", (pidStat)
                            print "Username :", stats['Username']
                            try:
                                print "Cmd name :", stats['Cmdline']
                                print "Status :", stats['Status']
                                print "CPU usage :", stats['Cpu'], "%"
                                print "Memory usage :", stats['Memory'], "%"
                                print "For close, press 'q'."
                                time.sleep(1)
                                os.system('clear')
                                if isData():#{
                                    realtime = sys.stdin.read(1)
                                    if realtime == 'q' or realtime == 'Q':
                                        break
                            #}
                        #}
                            except psutil.AccessDenied:
                                print "You don't have the right too see more details than that for this process."
                        except psutil.NoSuchProcess:
                            print "The process has been closed."
                            return (0)
                #}
                finally:
                    termios.tcsetattr(sys.stdin,termios.TCSADRAIN, old_settings)
            #}
            else:
                print "No process found with the PID \"{}\".".format(pidStat)
                return (0)
    #}
        except OverflowError:
            print "No process found with the pid \"{}\".".format(pidStat)
            return (0)
    except (NameError, TypeError, SyntaxError):
        print "The input need a valid integer, the Pid of a process."
        return (0)
        os.system('setterm -term linux -back black -fore white')
    return (1)
#}

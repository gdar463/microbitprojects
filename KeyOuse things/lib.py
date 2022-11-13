import os
import platform
import psutil
import socket
import time

def initCountdown(num):
    for(x) in range(num):
        x = (num-x)
        print(x)
        time.sleep(1)
    print("GO")

def detectOs():
    osStr = platform.system()
    if osStr == "Windows":
        osAlias = "win"
    elif osStr == "Linux":
        osAlias = 'linux'
    elif osStr == "macOS":
        osAlias = "mac"
    else:
        osAlias = "unknown"
    return osAlias

def shutdown(str):
    if str == "win":
        hostname = socket.gethostname()
        os.system("shutdown /s /m \\\\" + hostname + " /t 10 /c \"Bye\"")
    elif str == "linux" or str == "mac":
        os.system("sudo shutdown -h now \"Bye\"")

def goodbye():
    osStrs = detectOs()
    shutdown(osStrs)
    exit()

def checkIfProcRunning(processName):
    for proc in psutil.process_iter():
        try:
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False
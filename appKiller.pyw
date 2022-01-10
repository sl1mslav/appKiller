import os
import time
import psutil


def killApps():
    while True:
        for app in apps:
            os.system(f"TASKKILL /F /IM {app}")
        time.sleep(10)


def checkIfProcessRunning(processName):
    for proc in psutil.process_iter():
        try:
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


def giveActualDate():
    return int(time.strftime(format("%j")))


'''
Put the .exe files you want to limit the usage of in here:
'''

apps = ["RiotClientServices.exe", "steam.exe", "tld.exe", "EpicGamesLauncher.exe", "TLauncher.exe",
        "GenshinImpact.exe", "Discord.exe", "VALORANT.exe", "League of Legends.exe"]

'''
The desired allowed time of usage in minutes:
'''
allowedTime = 180

f = open("check.txt", "r")
text = f.read()
dateFromFile = int(text.split("\n")[0])
timeSpent = int(text.split("\n")[1])
f.close()
if giveActualDate() == dateFromFile and timeSpent >= allowedTime:
    killApps()
elif giveActualDate() != dateFromFile:
    f = open("check.txt", "w")
    f.write(str(giveActualDate()) + "\n")
    f.write("0")
    f.close()
while True:
    if timeSpent <= allowedTime:
        flag = False
        for app in apps:
            if checkIfProcessRunning(app):
                flag = True
        if flag:
            timeSpent += 1
            flag = False
        if timeSpent % 3 == 0:
            f = open("check.txt", "w")
            f.write(str(giveActualDate()) + "\n")
            f.write(str(timeSpent))
            f.close()
        time.sleep(60)
    else:
        killApps()

from api.lib.ToolKits.LogProcess import *
from api.lib.ToolKits.Event import *
import os
import sys
netWorkLogger=LogProcessor(f"{os.path.dirname(sys.argv[0])}/log/networkLog.txt")
downloadLogger=LogProcessor(f"{os.path.dirname(sys.argv[0])}/log/downloadLog.txt")


def doEvent_logDownloadWork(data):
    downloadLogger.append(LogMessage(data).message)
def doEvent_logNetWork(data):
    netWorkLogger.append(LogMessage(data).message)

def setup_log():
    addEvent('logNetWork',doEvent_logNetWork)
    addEvent('logDownloadWork',doEvent_logDownloadWork)


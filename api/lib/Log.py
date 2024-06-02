from api.lib.ToolKits.LogProcess import *
from api.lib.ToolKits.Event import *
import os

netWorkLogger=LogProcessor(f"{os.path.dirname(__file__)}/../../log/networkLog.txt")
downloadLogger=LogProcessor(f"{os.path.dirname(__file__)}/../../log/downloadLog.txt")

def doEvent_logDownloadWork(data):
    downloadLogger.append(LogMessage(data).message)
def doEvent_logNetWork(data):
    netWorkLogger.append(LogMessage(data).message)

def setup_log():
    addEvent('logNetWork',doEvent_logNetWork)
    addEvent('logDownloadWork',doEvent_logDownloadWork)


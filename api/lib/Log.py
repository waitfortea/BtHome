from api.lib.ToolKits.LogProcess import *
from api.lib.ToolKits.Event import *
import os

netWorkLogger=LogProcessor(f"{os.path.dirname(__file__)}/../../log/networkLog.txt")
downloadLogger=LogProcessor(f"{os.path.dirname(__file__)}/../../log/downloadLog.txt")

def doEvent_logNetWork(data):
    netWorkLogger.append(LogMessage(data).message)

def setup_logNetWork():
    addEvent('logNetWork',doEvent_logNetWork)

# callEvent('logNetWork',{"1":1})

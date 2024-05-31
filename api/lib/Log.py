from api.lib.ToolKits.LogProcess import *
from api.lib.ToolKits.Event import *
from datetime import datetime
log=LogProcessor("../../log/networkLog.txt")

def doEvent_logNetWork(message):
    message=datetime().now().strftime()+message
    log.append(message)
def setup_logNetWork():
    addEvent('logNetWork',doEvent_logNetWork)
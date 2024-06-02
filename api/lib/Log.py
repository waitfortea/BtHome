from api.lib.ToolKits.LogProcess import *
from api.lib.ToolKits.Event import *
from datetime import datetime
import os


logger=LogProcessor(f"{os.path.dirname(__file__)}/../../log/networkLog.txt")
def doEvent_logNetWork(message):
    text=" ".join([f'{key}:{value}' for key,value in message.items()])
    timeStamp=datetime.now().strftime("%Y/%m/%d %H:%M:%S")
    logger.append(timeStamp+" "+text+"\n")

def setup_logNetWork():
    addEvent('logNetWork',doEvent_logNetWork)

# callEvent('logNetWork',{"1":1})

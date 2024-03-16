import asyncio

from Event import subscribe,domain,tasks_List
from ToolKits.GeneralStrategy import AsyncStrategy
from Log import log

def setLogListener():
    subscribe('printLog',handleEvnetPrintLog)

def handleEvnetPrintLog(data):
    log(data)

def setDomainListener():
    subscribe('getDomain',handleEvnetGetDomain)

def handleEvnetGetDomain(data):
    return domain

# def setTasksListener():
#     subscribe('executeTasks',handleEventExecuteTasks)
#
#
#
# def handleEventExecuteTasks(data):
#     results=AsyncStrategy.execute(asyncGather(tasks_List))
#     return results



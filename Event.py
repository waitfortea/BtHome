import ToolKits.GeneralStrategy as GS
import aiohttp
import requests

import DomainCheck as DC


subscribers=dict()

domain=GS.AsyncStrategy().execute(DC.domain_check())
asyncSession=aiohttp.ClientSession()
syncSession=requests.Session()
tasks_List=[]
def subscribe(eventType:str, eventFn):
     if not eventType in subscribers:
         subscribers[eventType]=[]
     subscribers[eventType].append(eventFn)

def postEvent(eventType:str,data=None):
    if not eventType in subscribers:
        return
    for eventFn in subscribers[eventType]:
        return eventFn(data)
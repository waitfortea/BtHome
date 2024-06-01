from api.lib.ToolKits.Strategy.AsyncStrategy import *
from api.lib.ToolKits.SerializeProcessor import YamlProcessor
from api.lib.ToolKits.RequestsProcess import *
import aiohttp
import asyncio
import time
from api.lib.ToolKits.Event import *
from api.lib.ToolKits.Proxy import *

@dataclass
class Domain:
    address:str


domain=Domain("")

async def domainCheck(path=None):

    global domain

    domain_list=YamlProcessor("../../config/config.yaml").contentDict['domain_List']

    if not path:
        tasks = [asyncio.create_task(AsyncRequestsProcessor(url=i, session=aiohttpSession,proxy=globalProxy.proxy_aiohttp).response()) for i in domain_list]
    else:
        tasks = [asyncio.create_task(AsyncRequestsProcessor(url=i+'/'+path, session=aiohttpSession,proxy=globalProxy.proxy_aiohttp).response()) for i in domain_list]
    res=await firstComplete(tasks)

    domain.address = str(res.url)
    print(f'发起:{res.}返回{domain.address}')


def doEvent_domainCheck(path=None):
    round=0
    while "btbtt" not in domain.address:
        round += 1
        print(f'round{round}')
        try:
            asyncStrategy(domainCheck(path))
        except Exception as e:
            setProxy()
            asyncStrategy(domainCheck(path))

    print(f'可用域名:{domain.address}')

def setup_domainCheck():
    addEvent("domainCheck",doEvent_domainCheck)


setup_domainCheck()
callEvent("domainCheck",data="")




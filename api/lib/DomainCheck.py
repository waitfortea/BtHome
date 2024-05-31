
from api.lib.ToolKits.Strategy.AsyncStrategy import asyncStrategy,firstComplete
from api.lib.ToolKits.SerializeProcessor import YamlProcessor
from api.lib.ToolKits.RequestsProcess import *
import aiohttp
import asyncio
import time
from api.lib.ToolKits.Event import *
from api.lib.ToolKits.Proxy import *
from api.lib.Log import *
@dataclass
class Domain:
    address:str

domain=Domain("")

async def domainCheck(path=None):

    global domain

    domain_list=YamlProcessor("../../config/config.yaml").contentDict['domain_List']

    async def check(url):
        res=await AsyncRequestsProcessor(url=url, session=aiohttpSession, proxy=globalProxy.proxy_aiohttp).response()

    if not path:
        tasks = [asyncio.create_task(check(i)) for i in domain_list]
    else:
        tasks = [asyncio.create_task(AsyncRequestsProcessor(url=i+'/'+path, session=aiohttpSession,proxy=globalProxy.proxy_aiohttp).response()) for i in domain_list]
    res=await firstComplete(tasks)

    domain.address = str(res.url)


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
        print(f"返回域名为:{domain.address}")
    print(f'可用域名:{domain.address}')

def setup_domainCheck():
    addEvent("domainCheck",doEvent_domainCheck)

setProxy()
setup_domainCheck()
callEvent("domainCheck",data="")




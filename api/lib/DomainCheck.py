
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
        if "btbtt" not in str(res.url):
            domain_list.pop(url)
            return None
        return str(res.url)

    if not path:
        tasks = [asyncio.create_task(check(i)) for i in domain_list]
    else:
        tasks = [asyncio.create_task(check(url=i+'/'+path)) for i in domain_list]
    res=await firstComplete(tasks)

    domain.address = res


def doEvent_domainCheck(path=None):
    try:
        asyncStrategy(domainCheck(path))
    except Exception as e:
        setProxy()
        asyncStrategy(domainCheck(path))
    print(f'可用域名:{domain.address}')

def setup_domainCheck():
    addEvent("domainCheck",doEvent_domainCheck)

setProxy()
setup_domainCheck()
callEvent("domainCheck",data="")




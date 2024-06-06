
__all__='domain','domainCheck','doEvent_domainCheck','setup_domainCheck'

import asyncio
from api.lib.ToolKits.Strategy.AsyncStrategy import *
from api.lib.ToolKits.SerializeProcessor import *
from api.lib.ToolKits.RequestsProcess import *
from api.lib.ToolKits.Proxy import *
from dataclasses import dataclass
from api.lib.Config import *
@dataclass
class Domain:
    address:str

domain=Domain("")

async def domainCheck(path=None):

    global domain

    domain_list=config['domain_List']

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
    print(f'可用域名:{domain.address}')

def doEvent_domainCheck(path=None):
    asyncStrategy(domainCheck(path))


def setup_domainCheck():
    addEvent("domainCheck",doEvent_domainCheck)


if __name__=="__main__":
    pass








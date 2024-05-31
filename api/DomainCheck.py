
from api.lib.ToolKits.Strategy.AsyncStrategy import asyncStrategy,firstComplete
from api.lib.ToolKits.SerializeProcessor import YamlProcessor
from api.lib.ToolKits.RequestsProcess import *
import aiohttp
import asyncio
import time
from api.lib.ToolKits.Event import *


domain=""
proxy_aiohttp=None
proxy_request=None

async def domainCheck(path=None):

    global domain

    domain_list=YamlProcessor("./../config/config.yaml").contentDict['domain_List']

    if not path:
        tasks = [asyncio.create_task(AsyncRequestsProcessor(url=i, session=aiohttpSession,proxy=proxy_aiohttp).response()) for i in domain_list]
    else:
        tasks = [asyncio.create_task(AsyncRequestsProcessor(url=i+'/'+path, session=aiohttpSession,proxy=proxy_aiohttp).response()) for i in domain_list]
    res=await firstComplete(tasks)

    print(f'可用域名:{str(res.url)}')
    domain=str(res.url)

def doEvent_domainCheck(path=None):
    global proxy_request
    global proxy_aiohttp

    try:
        asyncStrategy(domainCheck(path))
    except Exception as e:
        proxy_aiohttp = "http://127.0.0.1:10809"
        proxy_request = {'http': "http://127.0.0.1:10809"
            , 'https': "http://127.0.0.1:10809"}
        asyncStrategy(domainCheck(path))

def setup_domainCheck():
    addEvent("domainCheck",doEvent_domainCheck)


setup_domainCheck()
callEvent("domainCheck",data="")



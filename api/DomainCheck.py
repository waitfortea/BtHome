
from api.lib.ToolKits.Strategy.AsyncStrategy import asyncStrategy,firstComplete
from api.lib.ToolKits.SerializeProcessor import YamlProcessor
from api.lib.ToolKits.RequestsProcess import *
import aiohttp
import asyncio
import time

domain=""
proxy_aiohttp=None
proxy_request=None

async def domainCheck(path=None):

    global domain

    domain_list=YamlProcessor("./../config/config.yaml").contentDict['domain_List']

    async with aiohttp.ClientSession() as session:
        if not path:
            tasks = [asyncio.create_task(AsyncRequestsProcessor(url=i, session=session,proxy=proxy_aiohttp).response()) for i in domain_list]
        else:
            tasks = [asyncio.create_task(AsyncRequestsProcessor(url=i+'/'+path, session=session,proxy=proxy_aiohttp).response()) for i in domain_list]
        res=await firstComplete(tasks)
        await session.close()

    print(f'可用域名:{res.url}')
    domain=res.url
    time.sleep(1)

try:
    asyncStrategy(domainCheck())
except Exception as e:
    proxy_aiohttp = "http://127.0.0.1:10809"
    proxy_request = {'http': "http://127.0.0.1:10809"
        , 'https': "http://127.0.0.1:10809"}
    asyncStrategy(domainCheck())


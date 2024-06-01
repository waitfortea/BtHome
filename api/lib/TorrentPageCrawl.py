import time
from abc import ABC, abstractmethod
import aiohttp
import requests
import re
import pandas as pd
import asyncio
from urllib.parse import quote, unquote
from api.lib.ToolKits.ElementProcess import *
from api.lib.ToolKits.Event import *
from api.lib.ToolKits.RequestsProcess import *
from api.lib.ToolKits.GeneralObject.StrProcess import *
from api.lib.ToolKits.DataStructure.ListProcess import *
from api.lib.ToolKits.Strategy.AsyncStrategy import *
from api.lib.ToolKits.Proxy import *
from api.CrawlObject import *
from api.lib.DomainCheck import *

async def getTorrentPageFromBtHome(index):
    while True:
        try:
            url = domain.address + "/" + f"search-index-keyword-{quote(index.keyword)}.htm"
            htmlText = RequestsProcessor(url, proxies=globalProxy.proxy_request).text()
            break
        except Exception as e:
            print(e)
            callEvent("domainCheck", data="")
            continue
    doc = ElementProcessor(htmlText)
    element_List = doc.xpath('//td[@class="subject"]//a[contains(text(),"BT")]')
    if element_List is None:
        print('搜索结果为空')
        return []
    async def getPageHtmlFromBtHome(index,session):

        htmlText = await AsyncRequestsProcessor(index.url, session=session, proxy=globalProxy.proxy_aiohttp).text()
        return TorrentPage(index=index, title=index.title, url=index.url,
                           htmlText=htmlText)

    tasks = [asyncio.create_task(getPageHtmlFromBtHome(Index(keyword=index.keyword,url=domain.address+"/"+element.attrib('href'),title=element.text()), session=aiohttpSession))
             for element in element_List]
    result_List = await allComplete(tasks)
    return result_List


async def getTorrentPageFromComicGarden(index):
    page_List=ListProcessor(index.page)

    async def getPageHtmlFromComicGarden(index, session):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.200',
        }
        params = {
            'keyword': index.keyword,
        }

        res = await AsyncRequestsProcessor(f'https://dmhy.org/topics/list/page/{index.page}', session=session,
                                           params=params, headers=headers, proxy=globalProxy.proxy_aiohttp).response()
        if res.status == 500:
            return None
        htmlText = await res.text()
        return htmlText

    tasks=[asyncio.create_task(getPageHtmlFromComicGarden(Index(keyword=index.keyword,page=page),aiohttpSession)) for page in page_List]
    result_List=await allComplete(tasks)
    TorrentPage_List=[TorrentPage(index=index, title=index.keyword, url=f'https://dmhy.org/topics/list/page',
                       htmlText=result_List)]
    return TorrentPage_List

if __name__=="__main__":
    # setProxy()
    # print(globalProxy.proxy_aiohttp)
    asyncStrategy(getTorrentPageFromBtHome(Index("迷宫饭")))
    closeSession(aiohttpSession)
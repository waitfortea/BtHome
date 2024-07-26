
__all__='getTorrentPageFromBtHome','getTorrentPageFromComicGarden'

import time

from api.lib.DomainCheck import *
from urllib.parse import quote, unquote
from api.lib.ToolKits.ElementProcess import *
from api.lib.ToolKits.Event import *
from api.lib.ToolKits.RequestsProcess import *
from api.lib.ToolKits.GeneralObject.StrProcess import *
from api.lib.ToolKits.DataStructure.ListProcess import *
from api.lib.ToolKits.Strategy.AsyncStrategy import *
from api.lib.ToolKits.Proxy import *
from api.lib.ToolKits.Proxy import *
from api.CrawlObject import *
import asyncio
from api.lib.cfcheck import *
from api.lib.Config import *
from api.lib.ToolKits.utils import *
async def getTorrentPageFromBtHome(index):
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
    }
    url = config['bthome_domain']+ f"/search-{quote(index.keyword).replace('%', '_')}.htm"
    print(url)
    callEvent("cf_check", {})
    count = counter()
    while True:
        try:
            htmlText = RequestsProcessor(url,session=requestSession,proxies=globalProxy.proxy_request, cookies=cf_cookies.cookies,headers = headers).text()
            print("torrentPageHtml获取")
            if "cloudflare" in htmlText:
                print("重新获取cf_cookies")
                callEvent("cf_check", {})
                continue
            else:
                break
        except Exception as e:
            print(f'{e} like html error')
            callEvent("cf_check", {})
            if count()>3:
                raise NotFoundResponse(url)




    doc = ElementProcessor(htmlText)
    # element_List = doc.xpath('//td[@class="subject"]//a[contains(@href,"thread-index") and @class="subject_link thread-old"]')
    element_List = doc.xpath('//div[@class="media-body"]//a[contains(@href,"thread")]')
    if element_List is None:
        print('搜索结果为空')
        return []

    async def getPageHtmlFromBtHome(index) -> List[TorrentPage]:

        htmlText = await AsyncRequestsProcessor(index.url, session=aiohttpSession, proxy=globalProxy.proxy_aiohttp,cookies=cf_cookies.cookies,headers = headers).text()
        return TorrentPage(index=index, title=index.title, url=index.url,
                           htmlText=htmlText,source= "BtHome")

    tasks = [asyncio.create_task(getPageHtmlFromBtHome(Index(keyword=index.keyword,url=config['bthome_domain']+"/"+element.attrib('href'),title=element.text())))
             for element in element_List]
    result_List = await allComplete(tasks)

    callEvent('bthome_insert_table_torrentpage',{
                "field_name":['url','title']
                ,"rows":[[torrent_page.url,torrent_page.title] for torrent_page in result_List]
                })
    return result_List


async def getTorrentPageFromComicGarden(index):
    page_List=ListProcessor(index.page)

    async def getPageHtmlFromComicGarden(index, session):
        headers = {

            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
        }
        params = {
            'keyword': index.keyword,
        }

        while True:
            try:
                res = await AsyncRequestsProcessor(f'https://dmhy.org/topics/list/page/{index.page}', session=session,
                                                   params=params, headers=headers, proxy=globalProxy.proxy_aiohttp,retry=3).response()
                break
            except Exception as e:
                raise e
                setProxy()
                continue

        if res.status == 500:
            return None
        htmlText = await res.text()
        return htmlText

    tasks=[asyncio.create_task(getPageHtmlFromComicGarden(Index(keyword=index.keyword,page=page),aiohttpSession)) for page in page_List]
    result_List=await allComplete(tasks)
    result_List=[result for result in result_List if result is not None]
    TorrentPage_List=[TorrentPage(index=index, title=index.keyword, url=f'https://dmhy.org/topics/list/page',
                       htmlText=result_List, source= "ComicGarden")]
    return TorrentPage_List

if __name__=="__main__":
    setProxy()
    # print(globalProxy.proxy_aiohttp)
    asyncStrategy(getTorrentPageFromBtHome(Index("迷宫饭",page=[i+1 for i in range(20)])))

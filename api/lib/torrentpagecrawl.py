
__all__='getTorrentPageFromBtHome','getTorrentPageFromComicGarden'

from urllib.parse import quote
from api.lib.ToolKits.parse.elementutils import *
from api.lib.ToolKits.request.requestutils import *
from api.lib.ToolKits.datastructure.listutils import *
from api.lib.ToolKits.coroutine.coroutineutils import *
from api.lib.ToolKits.proxy.proxyregister import *
from api.crawlobject import *
import asyncio
from api.lib.cfcheck import *
from api.lib.ToolKits.general.utils import *
from api.lib.brower import *
from api.http_process import *

def getTorrentPageFromBtHome(index):
    index.url = config['bthome_domain']
    index.title = 'BtHome'

    headers = {
        'user-agent': config['user_agent'],
    }
    url = config['bthome_domain']+ f"/search-{quote(index.keyword).replace('%', '_')}.htm"
    print(url)
    callEvent("cf_check", {})
    exception_count = counter()
    cfcheck_count = counter()


    htmlText = gethtml(url,headers=headers,cookies=None)
    # htmlText = RequestsProcessor(url,session=requestSession,proxies=globalProxy.proxy_request, cookies=cf_cookies.cookies,headers = headers).text()
    print("torrentPageHtml获取")



    doc = ElementProcessor(htmlText)
    # element_List = doc.xpath('//td[@class="subject"]//a[contains(@href,"thread-index") and @class="subject_link thread-old"]')
    element_List = doc.xpath('//div[@class="media-body"]//a[contains(@href,"thread")]')
    if element_List is None:
        print('搜索结果为空')
        return []

    result_List = [TorrentPage(index=index,url=config['bthome_domain']+"/"+torrentpage_element.attrib('href'),title=torrentpage_element.text()) for torrentpage_element in element_List]

    callEvent('bthome_insert_table_torrentpage',{
                "field_name":['url','title']
                ,"rows":[[torrent_page.url,torrent_page.title] for torrent_page in result_List]
                })
    return result_List


async def getTorrentPageFromComicGarden(index):
    page_List=ListProcessor(index.page)

    async def getPageHtmlFromComicGarden(index, session):
        headers = {

            'user-agent': config['user_agent'],
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
    async_strategy(getTorrentPageFromBtHome(Index("迷宫饭",page=[i+1 for i in range(20)])))

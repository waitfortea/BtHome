
from urllib.parse import quote
from api.lib.ToolKits.request import *
from api.lib.config import *
from api.lib.ToolKits.parse.elementutils import *
from api.lib.ToolKits.datastructure.listutils import *
from api.crawlobject import *
from api.bthomeutils import *

@BtHomeUtils.register_sourceplugin('bthome_search')
def bthome_searchplugin(keyword):
    headers = {
        'user-agent': config['user_agent'],
    }
    url = config['source']['bthome']['domain']+ f"/search-{quote(keyword).replace('%', '_')}.htm"

    htmlText = RequestUitls.get_html(name='drissionpage', type='get', url=url, headers=headers, cookies=None)

    doc = ElementUtils.parse_html(htmlText)

    element_List = doc.xpath('//div[@class="media-body"]//a[contains(@href,"thread")]')

    if not element_List:
        EventUtils.run('infolog',logdata='搜索结果为空')

    result_list = [TorrentPage(url=config['source']['bthome']['domain']+"/"+element.attrib['href']
                               , title=ElementUtils.get_text(element)) for element in element_List]
    return result_list


@BtHomeUtils.register_sourceplugin('comicgarden_search')
async def commicgarden_searchplugin(keyword):
    async def search(keyword, page):
        headers = {

            'user-agent': config['user_agent'],
        }
        params = {
            'keyword': keyword,
        }
        htmltext = RequestUitls.get_html(name='aiohttp'
                              , url=f"{config['source']['comicgarden']['domain']}/topics/list/page/{page}"
                              ,params=params
                              , headers=headers
                              , proxy=globalProxy.proxy_aiohttp,retry=3).response()

        return htmltext
    page_list = {}
    tasks=[asyncio.create_task(search(keyword, page)) for page in page_list]
    result_List=await asyncio.gather(tasks, return_exceptions=True)
    result_List=[result for result in result_List if result is not None]
    TorrentPage_List=[TorrentPage(index=index, title=index.keyword, url=f'https://dmhy.org/topics/list/page',
                       htmlText=result_List, source= "ComicGarden")]
    return TorrentPage_List

if __name__=="__main__":
    # print(globalProxy.proxy_aiohttp)
    EventUtils.run(eventname='loadconfig')
    EventUtils.run(eventname='loadbrowser', path=config['edge_exe_path'])
    #
    bthome_searchplugin(Index(keyword='进击'))

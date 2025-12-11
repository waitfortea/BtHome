
from urllib.parse import quote
from api.lib.ToolKits.request import *
from api.lib.config import *
from api.lib.ToolKits.parse.elementutils import *
from api.lib.ToolKits.datastructure.listutils import *
from api.crawlobject import *
from api.bthomeutils import *
from api.lib.ToolKits.coroutine import *

@BtHomeUtils.register_sourceplugin('bthome_search')
def bthome_searchplugin(keyword, page=1):
    headers = {
        'user-agent': config['user_agent'],
    }
    url = config['source']['bthome']['domain']+ f"/search-{quote(keyword).replace('%', '_')}-1-{page}.htm"

    htmlText = RequestUitls.get_html(name='dp_one_tab', type='get', url=url, headers=headers, cookies=None)

    doc = ElementUtils.parse_html(htmlText)

    element_List = doc.xpath('//div[@class="media-body"]//a[contains(@href,"thread")]')

    if not element_List:
        EventUtils.run('infolog',logdata='搜索结果为空')

    result_list = [TorrentPage(url=config['source']['bthome']['domain']+"/"+element.attrib['href']
                               , title=ElementUtils.get_text(element)) for element in element_List]
    return result_list

@BtHomeUtils.register_sourceplugin('bthome_batch_search')
def bthome_batch_searchplugin(keyword,page_range):
    headers = {
        'user-agent': config['user_agent'],
    }
    url_list = []
    for page in range(1,page_range+1):
        url  = config['source']['bthome']['domain'] + f"/search-{quote(keyword).replace('%', '_')}-1-{page}.htm"
        url_list.append(url)

    html_list= RequestUitls.get_html(name='dp_multi_tab', type='get', url_list=url_list, headers=headers, cookies=None)

    torrentpage_list = []
    for htmltext in html_list:
        doc = ElementUtils.parse_html(htmltext)

        element_List = doc.xpath('//div[@class="media-body"]//a[contains(@href,"thread")]')

        if not element_List:
            EventUtils.run('infolog', logdata='搜索结果为空')

        result_list = [TorrentPage(url=config['source']['bthome']['domain'] + "/" + element.attrib['href']
                                   , title=ElementUtils.get_text(element)) for element in element_List]
        torrentpage_list.append(result_list)
    return torrentpage_list


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
    bthome_expand_searchplugin(keyword='喜人奇妙夜2', page_range= 5)

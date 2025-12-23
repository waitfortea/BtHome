from typing import Any, List
from urllib.parse import quote
from api.lib.ToolKits.request import *
from api.lib.config import *
from api.lib.ToolKits.parse.elementutils import *
from api.lib.ToolKits.datastructure.listutils import *
from api.crawlobject import *
from api.bthomeutils import *
from api.lib.ToolKits.coroutine import *
import itertools

@BtHomeUtils.register_sourceplugin('bthome_search')
def bthome_searchplugin(keyword, page=1,*args, **kwargs):
    headers = {
        'user-agent': config['user_agent'],
    }
    url = config['source']['bthome']['domain']+ f"/search-{quote(keyword).replace('%', '_')}-1-{page}.htm"

    htmlText = RequestUitls.get_html(name='dp_one_tab', type='get', url=url)

    doc = ElementUtils.parse_html(htmlText)

    element_List = doc.xpath('//div[@class="media-body"]//a[contains(@href,"thread")]')

    if not element_List:
        EventUtils.run('infolog',logdata='搜索结果为空')

    result_list = [TorrentPage(url=config['source']['bthome']['domain']+"/"+element.attrib['href']
                               , title=ElementUtils.get_text(element)) for element in element_List]
    return result_list

@BtHomeUtils.register_sourceplugin('bthome_batch_search')
def bthome_batch_searchplugin(keyword: object, page_range: object, *args: object, **kwargs: object) -> List[Any]:

    url_list = []
    for page in range(1,page_range+1):
        url  = config['source']['bthome']['domain'] + f"/search-{quote(keyword).replace('%', '_')}-1-{page}.htm"
        url_list.append(url)

    html_list= RequestUitls.get_html(name='dp_multi_tab', type='get', url=url_list)

    torrentpage_list = []
    for htmltext in html_list:
        doc = ElementUtils.parse_html(htmltext)

        element_List = doc.xpath('//div[@class="media-body"]//a[contains(@href,"thread")]')

        if not element_List:
            EventUtils.run('infolog', logdata='搜索结果为空')

        result_list = [TorrentPage(url=config['source']['bthome']['domain'] + "/" + element.attrib['href']
                                   , title=ElementUtils.get_text(element)) for element in element_List]
        torrentpage_list.extend(result_list)

    return torrentpage_list

@BtHomeUtils.register_sourceplugin('bthome_multi_search')
def bthome_multi_searchplugin(keyword: object, page_range: object, *args: object, **kwargs: object) -> List[Any]:
    url_list = []
    for page in range(1, page_range + 1):
        url = re.sub("forum-17.*(?<=\.)",f"forum-17-{page}.",config['source']['bthome_multi']['domain'])
        url_list.append(url)


    html_list = RequestUitls.get_html(name='dp_multi_tab', type='get', url=url_list)

    torrentpage_list = []
    for htmltext in html_list:
        doc = ElementUtils.parse_html(htmltext)

        element_List = doc.xpath('//div[@class="media-body"]//a[contains(@href,"thread") and contains(@class,"text")]')

        if not element_List:
            EventUtils.run('infolog', logdata='搜索结果为空')

        result_list = [TorrentPage(url=config['source']['bthome']['domain'] + "/" + element.attrib['href']
                                   , title=ElementUtils.get_text(element)) for element in element_List]
        torrentpage_list.extend(result_list)

    return torrentpage_list


@BtHomeUtils.register_sourceplugin('comicgarden_search')
def commicgarden_searchplugin(keyword, page_range, *args, **kwargs):
    url_list = []
    for page in range(1, page_range + 1):
        url = f"{config['source']['comicgarden']['domain']}/topics/list/page/{page}?keyword={quote(keyword)}"
        url_list.append(url)

    html_list = RequestUitls.get_html(name='dp_multi_tab', type='get', url=url_list)


    return [TorrentPage(title=f"{keyword}_{page_range}", url=f'https://dmhy.org/topics/list/page',
                       htmltext=html_list)]

if __name__=="__main__":
    # print(globalProxy.proxy_aiohttp)
    config.loadconfig(rf'{re.search(".*BtHome", os.path.dirname(__file__)).group()}\config\config.yaml')
    EventUtils.run(eventname='loadbrowser', path=config['edge_exe_path'])
    #
    torrentpage_list = BtHomeUtils.search(keyword='喜人奇妙夜2', page_range= 5)
    print(len(torrentpage_list))

import asyncio
from api.crawlobject import *
from api.lib.ToolKits.parse.elementutils import *
from api.lib.ToolKits.coroutine.coroutineutils import *
from api.lib.ToolKits.general.strutils import *
from api.lib.ToolKits.request.requestutils import *
from api.lib.config import *
from api.bthomeutils import *


@BtHomeUtils.register_sourceplugin('bthome_sgget')
def bthome_sgparse(torrentpage):
    subtitlegroup_list=[]

    htmltext = RequestUitls.get_html(name='drissionpage', url=torrentpage.url, type='get', headers={'user-agent':config['user_agent']}, cookies=None)
    doc = ElementUtils.parse_html(htmltext)
    sgelement_list = doc.xpath('//fieldset[@class="fieldset"][.//a]')

    for sgelement in sgelement_list:
        torrentelement_list= sgelement.xpath('.//a')
        sg_name = " ".join([ElementUtils.get_text(p).replace("\t", "").replace("\n", "").strip()
                                      for p in sgelement.xpath('./preceding-sibling::p')]) \
                                      if sgelement.xpath('./ancestor::div[@class="message mt-1 break-all"]') else "主页"
        subtitlegroup_list.append(SubtitleGroup(name=sg_name,torrentelement_list=torrentelement_list,torrentpage=torrentpage))

    return subtitlegroup_list

@BtHomeUtils.register_sourceplugin('comicgarden_sgget')
async def comicgarden_sgparse(torrentpage):
    async def getSubtitleGroupByOnePage(htmltext):
        torrentLink_List = ElementUtils.parse_html(data=htmltext).xpath("//td[@class='title']/a")
        result_List=[]
        for torrentLink in torrentLink_List:
            torrentURL=torrentLink.attrib("href")
            subtileGroupElement = '其他' if torrentLink.xpath('./preceding-sibling::*[1]') == [] else torrentLink.xpath('./preceding-sibling::*[1]')[0]
            sg_name= StrUtils.toStrip(subtileGroupElement.text()).toStrip if subtileGroupElement != '其他' else '其他'
            result_List.append((sg_name,torrentURL))
        return result_List

    tasks = [asyncio.create_task(getSubtitleGroupByOnePage(htmltext)) for htmltext in torrentpage.htmltext]
    result_List = await asyncio.gather(tasks, return_exceptions=True)
    torrentInfo_List = ListUtils.join(result_List)


    torrentURL_List = []
    sg_name_List = []

    for result in torrentInfo_List:
        sg_name_List.append(result[0])
        torrentURL_List.append(result[1])

    subtitleGroup_Dict = listMatchByDict(sg_name_List,torrentURL_List)
    subtitlegroup_list = []
    for sg_name, torrentpageURL_List in subtitleGroup_Dict.items():
        subTitleGroup =SubtitleGroup(name=sg_name,torrentURL_List=torrentpageURL_List, torrent_page=torrentpage)
        subtitlegroup_list.append(subTitleGroup)
    return subtitlegroup_list

if __name__=="__main__":
    pass
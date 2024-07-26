
from api.CrawlObject import *
from api.lib.ToolKits.RequestsProcess import *
from api.lib.ToolKits.ElementProcess import *
from api.lib.ToolKits.DataStructure.ListProcess import *
from api.lib.ToolKits.Strategy.AsyncStrategy import *
from api.lib.ToolKits.GeneralObject.StrProcess import *
from api.lib.ToolKits.Proxy import *
import asyncio

async def getSubtitleGroupFromBtHome(torrentPage):
    subtitleGroup_List=[]
    htmlText = torrentPage.htmlText
    subtitleGroupElement_List = ElementProcessor(data=htmlText).xpath('//fieldset[@class="fieldset"][.//a]')

    for subtitleGroupElement in subtitleGroupElement_List:
        torrentElement_List= subtitleGroupElement.xpath('.//a')
        subtitleGroupName = " ".join([p.text().replace("\t", "").replace("\n", "").strip()
                                      for p in subtitleGroupElement.xpath('./preceding-sibling::p')]) \
                                      if subtitleGroupElement.xpath('./ancestor::div[@class="message mt-1 break-all"]') !=[] else "主页"
        subtitleGroup_List.append(SubtitleGroup(name=subtitleGroupName,torrentElement_List=torrentElement_List,superObj=torrentPage))

    # extraElement_List = ElementProcessor(data=htmlText).xpath('(//div[@class="attachlist"])[1]')
    # if extraElement_List[0].element.xpath("./preceding-sibling::*[@class='message']") == []:
    #     extraGroupElement = extraElement_List[0]
    #     extraTorrentElement_List=extraGroupElement.xpath('//a[contains(text(),".t")]')
    #     extraGroup=SubtitleGroup(name='主页',superObj=torrentPage,torrentElement_List=extraTorrentElement_List)
    #     subtitleGroup_List.insert(0,extraGroup)
    return subtitleGroup_List

async def getSubtitleGroupFromComicGarden(torrentPage):
    async def getSubtitleGroupByOnePage(htmlText):
        pageElement = ElementProcessor(data=htmlText)
        torrentLink__List = pageElement.xpath("//td[@class='title']/a")
        result_List=[]
        for torrentLink in torrentLink__List:
            torrentURL=torrentLink.attrib("href")
            subtileGroupElement = '其他' if torrentLink.xpath('./preceding-sibling::*[1]') == [] else torrentLink.xpath('./preceding-sibling::*[1]')[0]
            subtitleGroupName= StrProcessor(subtileGroupElement.text()).toStrip if subtileGroupElement != '其他' else '其他'
            result_List.append((subtitleGroupName,torrentURL))
        return result_List

    tasks = [asyncio.create_task(getSubtitleGroupByOnePage(htmlText)) for htmlText in torrentPage.htmlText]
    result_List = await allComplete(tasks)
    torrentInfo_List=concatList(result_List)


    torrentURL_List = []
    subtitleGroupName_List = []

    for result in torrentInfo_List:
        subtitleGroupName_List.append(result[0])
        torrentURL_List.append(result[1])

    subtitleGroup_Dict = listMatchByDict(subtitleGroupName_List,torrentURL_List)
    subtitleGroup_List = []
    for subtitleGroupName, torrentPageURL_List in subtitleGroup_Dict.items():
        subTitleGroup =SubtitleGroup(name=subtitleGroupName,torrentURL_List=torrentPageURL_List, superObj=torrentPage)
        subtitleGroup_List.append(subTitleGroup)
    return subtitleGroup_List

if __name__=="__main__":
    pass
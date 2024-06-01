from api.lib.ToolKits.ElementProcess import *
from api.CrawlObject import *
from api.lib.ToolKits.DataStructure.ListProcess import *
import asyncio

async def getSubTitleGroupsFromBtHome(torrentPage:TorrentPage):
    subtitleGroup_List=[]
    htmlText = torrentPage.htmlText
    subtitleGroupElement_List = ElementProcessor(data=htmlText).xpath("//td[@class='post_td']//div[@class='message']")

    for subtitleGroupElement in subtitleGroupElement_List:
        torrentElement_List= subtitleGroupElement.xpath('..//a[contains(text(),".torrent")]')
        subtitleGroupName = subtitleGroupElement.text().replace("\t", "").replace("\n", "").strip()
        subtitleGroup_List.append(SubtitleGroup(name=subtitleGroupName,torrentElement_List=torrentElement_List,superObj=torrentPage))

    extraElement_List = ElementProcessor(data=htmlText).xpath('(//div[@class="attachlist"])[1]')
    if extraElement_List[0].element.xpath("./preceding-sibling::*[@class='message']") == []:
        extraGroupElement = extraElement_List[0]
        extraTorrentElement_List=extraGroupElement.xpath('//a[contains(text(),".torrent")]')
        extraGroup=SubtitleGroup(name='主页',superObj=torrentPage,torrentElement_List=extraTorrentElement_List)
        subtitleGroup_List.insert(0,extraGroup)
    return subtitleGroup_List

async def getSubTitleGroupsFromComicGarden(TorrentPage):
    async def getSubtitleGroupsByOnePage(htmlText):
        pageElement = ElementProcessor(data=htmlText)
        torrentLink__List = pageElement.xpath("//td[@class='title']/a")
        result_List=[]
        for torrentLink in torrentLink__List:
            torrentURL=torrentLink.attrib("href")
            subtileGroupElement = '其他' if torrentLink.xpath('./preceding-sibling::*[1]') == [] else torrentLink.xpath('./preceding-sibling::*[1]')[0]
            subtitleGroupName= StrProcessor(subtileGroupElement.text()).toStrip if subtileGroupElement != '其他' else '其他'
            result_List.append((subtitleGroupName,torrentURL))
        return result_List

    tasks = [asyncio.create_task(getSubtitleGroupsByOnePage(htmlText)) for htmlText in TorrentPage.htmlText]
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
        subTitleGroup =SubtitleGroup(name=subtitleGroupName,torrentURL_List=torrentPageURL_List, superObj=TorrentPage)
        subtitleGroup_List.append(subTitleGroup)
    return subtitleGroup_List

if __name__=="__main__":
    pass
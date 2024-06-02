from api.CrawlObject import *
from api.lib.ToolKits.RequestsProcess import *
from api.lib.ToolKits.ElementProcess import *
from api.lib.ToolKits.DataStructure.ListProcess import *
from api.lib.ToolKits.Strategy.AsyncStrategy import *
from api.lib.ToolKits.Proxy import *
import asyncio
async def getTorrentFromBtHome(subtileGroup):
    torrent_List=[]
    for torrentElement in subtileGroup.torrentElement_List:
        torrentName = torrentElement.text()
        torrentURL= torrentElement.attrib('href').replace('dialog', 'download')
        torrent = Torrent(name=torrentName, downloadURL=torrentURL)
        torrent_List.append(torrent)

    return TorrentGroup(torrent_List=torrent_List, superObj=subtileGroup)
async def getTorrentFromComicGarden(subtitleGroup:SubtitleGroup):
    torrent_List = []
    async def getTorrent(url):
        htmlText=await AsyncRequestsProcessor("https://dmhy.org"+url,session=aiohttpSession,proxy=globalProxy.proxy_aiohttp).text()
        torrent_List=ElementProcessor(htmlText).xpath("//a[contains(@href,'.torrent')]")
        return torrent_List

    tasks=[asyncio.create_task(getTorrent(url)) for url in subtitleGroup.torrentURL_List]
    result_List=await allComplete(tasks)
    torrentElement_List=concatList(result_List)
    for torrentElement in torrentElement_List:
        torrentName=torrentElement.text()
        downloadURL=torrentElement.attrib('href')
        torrent_List.append(Torrent(name=torrentName,downloadURL=downloadURL))
    return TorrentGroup(torrent_List=torrent_List,superObj=subtitleGroup)

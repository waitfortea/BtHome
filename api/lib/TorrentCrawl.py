import os.path

from api.CrawlObject import *
from api.lib.ToolKits.RequestsProcess import *
from api.lib.ToolKits.ElementProcess import *
from api.lib.ToolKits.DataStructure.ListProcess import *
from api.lib.ToolKits.Strategy.AsyncStrategy import *
from api.lib.ToolKits.Proxy import *
from api.lib.ToolKits.GeneralObject.StrProcess import *
import asyncio
from api.lib.DomainCheck import *
from api.lib.ToolKits.FileProcess import *
async def getTorrentGroupFromBtHome(subtileGroup):
    torrent_List=[]
    for torrentElement in subtileGroup.torrentElement_List:
        torrentName = verifyFileName(torrentElement.text())
        if os.path.splitext(torrentName)[-1] not in [".torrent",'.rar']:
            pass
        else:
            torrentName=os.path.splitext(torrentName)[0]

        torrentURL= domain.address+"/"+torrentElement.attrib('href').replace('dialog', 'download')
        torrent = Torrent(name=torrentName, downloadURL=torrentURL)
        torrent_List.append(torrent)

    return TorrentGroup(torrent_List=torrent_List, superObj=subtileGroup)
async def getTorrentGroupFromComicGarden(subtitleGroup:SubtitleGroup):
    torrent_List = []
    async def getTorrent(url):
        htmlText=await AsyncRequestsProcessor("https://dmhy.org"+url,session=aiohttpSession,proxy=globalProxy.proxy_aiohttp).text()
        torrent_List=ElementProcessor(htmlText).xpath("//a[contains(@href,'.torrent')]")
        return torrent_List

    tasks=[asyncio.create_task(getTorrent(url)) for url in subtitleGroup.torrentURL_List]
    result_List=await allComplete(tasks)
    torrentElement_List=concatList(result_List)
    for torrentElement in torrentElement_List:
        torrentName=verifyFileName(torrentElement.text())
        downloadURL=torrentElement.attrib('href')
        torrent_List.append(Torrent(name=torrentName,downloadURL=downloadURL))
    return TorrentGroup(torrent_List=torrent_List,superObj=subtitleGroup)

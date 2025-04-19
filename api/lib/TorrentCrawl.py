import asyncio
from api.CrawlObject import *
from api.lib.ToolKits.parseutils.elementutils import *
from api.lib.ToolKits.strategy.AsyncStrategy import *
from api.lib.ToolKits.generalutils.strutils import *
from api.http_process import *
from api.lib.ToolKits.generalutils.fileutils import *
from api.lib.Config import *

async def getTorrentGroupFromBtHome(subtileGroup):
    torrent_List=[]
    for torrentElement in subtileGroup.torrentElement_List:
        torrentName = verifyFileName(torrentElement.text()).replace("\n","")
        torrentURL= config['bthome_domain']+"/"+torrentElement.attrib('href')
        torrent = Torrent(name=torrentName, downloadURL=torrentURL,subtitle_group=subtileGroup)
        torrent_List.append(torrent)

    return TorrentGroup(torrent_List=torrent_List, subtitle_group=subtileGroup)


async def getTorrentGroupFromComicGarden(subtitleGroup:SubtitleGroup):
    torrent_List = []
    async def getTorrent(url):
        htmlText=await gethtml("https://dmhy.org"+url,strategy=aiohttp_html_strategy,retry=3).text()
        torrent_List=ElementProcessor(htmlText).xpath("//a[contains(@href,'.torrent')]")
        return torrent_List

    tasks=[asyncio.create_task(getTorrent(url)) for url in subtitleGroup.torrentURL_List]
    result_List=all_complete(tasks)
    torrentElement_List=concatList(result_List)
    for torrentElement in torrentElement_List:
        torrentName=verifyFileName(torrentElement.text())
        downloadURL="https:"+torrentElement.attrib('href')
        torrent_List.append(Torrent(name=torrentName,downloadURL=downloadURL))
    return TorrentGroup(torrent_List=torrent_List,subtitle_group=subtitleGroup)

__all__="torrentFilterByKeyword",'getTorrentContent','torrentDownload'

import asyncio
from dataclasses import  dataclass
from api.lib.ToolKits.GeneralObject.StrProcess import *
from api.lib.ToolKits.RequestsProcess import *
from api.lib.ToolKits.CustomException import *
from api.lib.ToolKits.CustomType import *
from api.lib.ToolKits.Strategy.AsyncStrategy import *
from api.lib.ToolKits.Proxy import *
from api.lib.ToolKits.FileProcess import *
from api.CrawlObject import *
from api.lib.DomainCheck import *
import aiofiles
import bencodepy

torrentDownloadingQueue=[]

def torrentFilterByKeyword(torrentGroup:TorrentGroup,keyWord):
    word_List=keyWord.split(" ")
    result_List=[torrent for torrent in torrentGroup.torrent_List if StrProcessor(torrent.name).contains(word_List,mode='all')]
    return TorrentGroup(torrent_List=result_List,superObj=torrentGroup.superObj)

def doEvent_waitDownload(torrentGourp,downloadPath):
    global torrentDownloadingQueue
    downloadPath = pathInit(downloadPath,type="dir").absolutePath
    torrentDownloadingQueue.append({'torrentGroup':torrentGourp,'downloadPath':downloadPath})

async def getTorrentContent(torrent:Torrent):
        count=0
        while True and count < 10:
            try:
                res=await AsyncRequestsProcessor(domain.address + '/' + torrent.url, proxy=globalProxy.proxy_aiohttp)
                torrentContent_IO = await res.content.read()
                torrentContent = bencodepy.decode(torrentContent_IO)
                break
            except Exception as e:
                print(e)
                count += 1
                print(f'重新获取{count}')
                if count >= 5:
                    callEvent('domainCheck',"")
        return torrentContent

async def torrentDownload(torrent,downloadPath):

    file=pathInit(downloadPath,flag="dir",make=True)
    downloadPath=file.absolutePath
    torrentName_List = [file.fileName for file in
                        file.parDir.getFileListBySuffix(['.torrent'])]

    if torrent.name in torrentName_List:
        return

    torrentContent = await getTorrentContent(torrent)
    async with aiofiles.open(rf'{downloadPath}\{torrent.name}', mode='wb') as file:
        await file.write(bencodepy.encode(torrentContent))

async def torrentGroupDownload(task):
    torrentGroup=getTorrentContent(task['torrentGroup'])
    downloadPath=task['downloadPath']
    tasks=[asyncio.create_task(torrentDownload(torrent,downloadPath)) for torrent in torrentGroup.torrent_List]
    await allComplete(tasks)

async def queueDownload():
    tasks=[asyncio.create_task(torrentGroupDownload(task)) for task in torrentDownloadingQueue]
    await allComplete(tasks)
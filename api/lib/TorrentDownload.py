__all__="torrentFilterByKeyword",'getDownloadContent','torrentDownload','waitDownload','torrentDownloadingQueue','queueDownload'

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

def torrentFilterByKeyword(torrentGroup:TorrentGroup,word_List):
    result_List=[torrent for torrent in torrentGroup.torrent_List if StrProcessor(torrent.name).contains(word_List,mode='all')]
    return TorrentGroup(torrent_List=result_List,superObj=torrentGroup.superObj)

def waitDownload(torrentGroup:TorrentGroup,downloadPath):
    global torrentDownloadingQueue
    downloadPath = pathInit(downloadPath,flag="dir",make=True).absolutePath
    torrentDownloadingQueue.append({'torrentGroup':torrentGroup,'downloadPath':downloadPath})

    message={
        '任务类型':'添加等待下载任务'
         ,'字幕组名称':torrentGroup.superObj.name
        , '下载源':torrentGroup.superObj.superObj.url
        ,'下载目录': downloadPath
        ,'种子数':len(torrentGroup.torrent_List)
    }
    callEvent("logDownloadWork",message)

async def getDownloadContent(torrent:Torrent):
        count=0
        while True and count < 10:
            try:
                res=await AsyncRequestsProcessor(torrent.downloadURL, session=aiohttpSession,proxy=globalProxy.proxy_aiohttp).response()
                suffix=getResFileSuffix(res)
                Content_IO = await res.content.read()
                # if suffix==".torrent":
                #     downloadContent = bencodepy.encode(bencodepy.decode(Content_IO))
                # else:
                #     downloadContent = Content_IO
                break
            except Exception as e:
                print(e)
                count += 1
                print(f'重新获取{count}')
                if count >= 5:
                    callEvent('domainCheck',"")
        return Content_IO,suffix

async def torrentDownload(torrent,downloadPath):

    download_dir=pathInit(downloadPath,flag="dir",make=True)
    downloadPath=download_dir.absolutePath
    torrentName_List = [file.fileName for file in
                        download_dir.getFileListBySuffix(['.torrent'])]

    if torrent.name in torrentName_List:
        return

    content,suffix = await getDownloadContent(torrent)
    async with aiofiles.open(rf'{downloadPath}\{torrent.name}{suffix}', 'wb') as file:
        await file.write(content)
    return rf'{downloadPath}\{torrent.name}{suffix}'

async def torrentGroupDownload(task):

    torrentGroup=task['torrentGroup']
    downloadPath=task['downloadPath']

    message = {
        '任务类型': '开始下载'
        , '字幕组名称': torrentGroup.superObj.name
        , '下载源': torrentGroup.superObj.superObj.url
        , '下载目录': downloadPath
        , '种子列表':"\n".join([torrent.name for torrent in torrentGroup.torrent_List])
    }
    callEvent("logDownloadWork", message)

    tasks=[asyncio.create_task(torrentDownload(torrent,downloadPath)) for torrent in torrentGroup.torrent_List]
    torrentGroupPath_List=await allComplete(tasks)
    return torrentGroupPath_List

async def queueDownload():
    print("------Download------")
    print("开始下载")
    tasks=[asyncio.create_task(torrentGroupDownload(task)) for task in torrentDownloadingQueue]
    torrentAdditionQueue=await allComplete(tasks)
    torrentDownloadingQueue.clear()
    print("下载完成")
    return torrentAdditionQueue



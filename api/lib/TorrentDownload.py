__all__ = "torrentFilterByKeyword", 'getDownloadContent', 'torrentDownload', 'waitDownload', 'torrentDownloadingQueue', 'queueDownload'

import asyncio
from dataclasses import dataclass
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
from api.lib.cfcheck import *

torrentDownloadingQueue = []


def torrentFilterByKeyword(torrentGroup: TorrentGroup, word_List):
    result_List = [torrent for torrent in torrentGroup.torrent_List if
                   StrProcessor(torrent.name).contains(word_List, mode='all')]
    return TorrentGroup(torrent_List=result_List, superObj=torrentGroup.superObj)


def waitDownload(torrentGroup: TorrentGroup, downloadPath):
    global torrentDownloadingQueue
    downloadPath = pathInit(downloadPath, flag="dir", make=True).absolutePath
    torrentDownloadingQueue.append({'torrentGroup': torrentGroup, 'downloadPath': downloadPath})

    message = {
        '任务类型': '添加等待下载任务'
        , '字幕组名称': torrentGroup.superObj.name
        , '下载源': torrentGroup.superObj.superObj.url
        , '下载目录': downloadPath
        , '种子数': len(torrentGroup.torrent_List)
    }
    callEvent("logDownloadWork", message)


async def getDownloadContent(torrent: Torrent):
    headers = {

        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
    }
    print(torrent.downloadURL)
    print(cf_cookies.cookies)
    res = await AsyncRequestsProcessor(torrent.downloadURL, session=aiohttpSession,
                                       proxy=globalProxy.proxy_aiohttp,cookies=cf_cookies.cookies,headers=headers).response()
    suffix = getResFileSuffix(res)

    if suffix not in [".torrent",'.rar']:
        suffix = ".torrent"

    Content_IO = await AsyncRequestsProcessor(torrent.downloadURL, session=aiohttpSession,
                                       proxy=globalProxy.proxy_aiohttp,cookies=cf_cookies.cookies,headers=headers).content()
    print(Content_IO)
    return Content_IO, ".torrent"


async def torrentDownload(torrent, downloadPath):

    content, suffix = await getDownloadContent(torrent)
    async with aiofiles.open(rf'{downloadPath}\{torrent.name}{suffix}', 'wb') as file:
        await file.write(content)
    return rf'{downloadPath}\{torrent.name}{suffix}'


async def torrentGroupDownload(task):
    torrentGroup = task['torrentGroup']
    downloadPath = task['downloadPath']

    download_dir = pathInit(downloadPath, flag="dir", make=True)
    torrentName_List = [file.baseName for file in
                        download_dir.get_direct_file_bySuffix(['.torrent'])]

    ignore_torrentname_List = []
    download_torrent_List = []
    for torrent in torrentGroup.torrent_List:
        if torrent.name not in torrentName_List:
            download_torrent_List.append(torrent)
        else:
            ignore_torrentname_List.append(torrent.name)

    if ignore_torrentname_List != []:
        ignore_message = {
            '任务类型': '忽略已存在种子'
            , '字幕组名称': torrentGroup.superObj.name
            , '下载源': torrentGroup.superObj.superObj.url
            , '下载目录': download_dir.absolutePath
            , '种子列表': "\n".join(ignore_torrentname_List)
        }
        callEvent("logDownloadWork", ignore_message)

    if download_torrent_List != []:
        download_message = {
            '任务类型': '开始下载'
            , '字幕组名称': torrentGroup.superObj.name
            , '下载源': torrentGroup.superObj.superObj.url
            , '下载目录': download_dir.absolutePath
            , '种子列表': "\n".join([f'{torrent.name} {torrent.downloadURL}' for torrent in download_torrent_List]) if download_torrent_List != [] else  "空"
        }
        callEvent("logDownloadWork", download_message)

        tasks = [asyncio.create_task(torrentDownload(torrent, download_dir.absolutePath)) for torrent in download_torrent_List]
        torrentGroupPath_List = await allComplete(tasks)
        return torrentGroupPath_List
    else:
        return []


async def queueDownload():
    print("------Download------")
    print("开始下载")
    tasks = [asyncio.create_task(torrentGroupDownload(task)) for task in torrentDownloadingQueue]
    torrentAdditionQueue = await allComplete(tasks)
    torrentDownloadingQueue.clear()
    print("下载完成")
    return torrentAdditionQueue

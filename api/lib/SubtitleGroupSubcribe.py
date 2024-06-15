
__all__ = "subscribe",'update'

import asyncio
from threading import Thread
from api.lib.ToolKits.Download.QbittorrentProcess import addTorrentInBatch
from api.lib.ToolKits.SerializeProcessor import *
from api.lib.ToolKits.FileProcess import *
from api.lib.ToolKits.Strategy.AsyncStrategy import *
from api.lib.ToolKits.CustomException import *
from api.CrawlObject import *
from api.lib.TorrentDownload import *
import os
import sys
from api.BtProcess import *
from api.lib.DomainCheck import *

def subscribe(torrentGroup,word_List,download_dir):
    subscribe_dir = pathInit(f'{os.path.dirname(sys.argv[0])}/subscribe', make=True, flag="dir")
    subscription = SubtitleSubscription(index=torrentGroup.superObj.superObj.index
                                        , torrent_page_url=torrentGroup.superObj.superObj.url
                                        , subtitle_group_name=torrentGroup.superObj.name
                                        , word_List=word_List
                                        , source = torrentGroup.superObj.superObj.source
                                        ,download_dir =download_dir
                                        )
    serializeByPickle(f'{subscribe_dir.absolutePath}/{torrentGroup.superObj.superObj.index.keyword}.txt', subscription)

async def updateTorrentPageFromBtHome(subscription):
    htmlText = await AsyncRequestsProcessor(subscription.torrent_page_url,session=aiohttpSession,proxy = globalProxy.proxy_aiohttp).text()
    return TorrentPage(index = subscription.index, source = "BtHome", title = "更新" , url = subscription.torrent_page_url, htmlText=htmlText)


async def updateTorrentPageFromComicGarden(subscription):
    torrentPage_List = await getTorrentPageFromComicGarden(subscription.index)
    return torrentPage_List[0]

async def update(word_List=None,mode="all"):
    await domainCheck()

    strategy_Dict = {
        "BtHome": {
            'torrentPageStrategy': updateTorrentPageFromBtHome
            , 'subtitleGroupStrategy': getSubtitleGroupFromBtHome
            , 'torrentGroupStrategy': getTorrentGroupFromBtHome
        }
        , "ComicGarden": {
            'torrentPageStrategy': updateTorrentPageFromComicGarden
            , 'subtitleGroupStrategy': getSubtitleGroupFromComicGarden
            , 'torrentGroupStrategy': getTorrentGroupFromComicGarden
        }

    }
    subscribe_dir = pathInit(f'{os.path.dirname(sys.argv[0])}/subscribe', make=True, flag="dir")

    if word_List != []:
        subscription_List = subscribe_dir.directFiles
    else:
        subscription_List = subscribe_dir.get_direct_file_byContainMode(word_List,mode=mode)

    async def updateTask(file):

        subscription = deserializeByPickle(file.absolutePath)

        if "index" not in dir(subscription):
            raise DictKeyError("index")

        torrentPage = await strategy_Dict[subscription.source]['torrentPageStrategy'](subscription)
        subtileGroup = [subtitle_group for subtitle_group in await strategy_Dict[subscription.source]['subtitleGroupStrategy'](torrentPage) if subscription.subtitle_group_name == subtitle_group.name][0]
        torrentGroup = await strategy_Dict[subscription.source]['torrentGroupStrategy'](subtileGroup)
        torrentGroup = torrentGroup if subscription.word_List is  None else torrentFilterByKeyword(torrentGroup,subscription.word_List)
        waitDownload(torrentGroup,subscription.download_dir)

    tasks = [asyncio.create_task(updateTask(file)) for file in subscription_List]
    await allComplete(tasks)

    try:
        torrentAddition_List = await queueDownload()
        addThread = Thread(target=addTorrentInBatch, args=(qbClient, torrentAddition_List))
        addThread.start()
        addThread.join()
    except Exception as e:
        print(e)
        raise e

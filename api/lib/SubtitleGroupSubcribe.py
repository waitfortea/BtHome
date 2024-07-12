
__all__ = "subscribe",'update','view_subscription'

import asyncio
import types
from threading import Thread
from api.lib.ToolKits.GeneralObject.urlporcess import *
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
from api.lib.ToolKits.utils import *
from api.lib.cfcheck import *

def view_subscription(subscription :SubtitleSubscription,depth= 3):

    def dfs(obj,prop = None,_depth = -1):
        _depth += 1
        sep ="  " * _depth

        if _depth > depth:
            return
        if isinstance(prop,str):
            if isinstance(getattr(obj,prop),str):
                print(f'{sep} {prop}:{getattr(obj,prop)}')
                return
            elif isinstance(getattr(obj, prop), types.MethodType):
                return
            else:
                obj = getattr(obj,prop)

        property_list = [i for i in dir(obj) if not i.startswith("__")]
        for i in range(len(property_list)):
            dfs(obj,property_list[i],_depth)

    dfs(subscription)




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
    count = counter()
    while count()<3:
        htmlText = await AsyncRequestsProcessor(URLProcessor(subscription.torrent_page_url).url
                                                ,session=aiohttpSession,proxy = globalProxy.proxy_aiohttp
                                                ,cookies=cf_cookies.cookies
                                                ,headers = cf_cookies.headers).text()
        if "Just a moment" in htmlText:
            callEvent("cf_check",{})
            continue
        else:
            break

    return TorrentPage(index = subscription.index, source = "BtHome", title = "更新" , url = subscription.torrent_page_url, htmlText=htmlText)

async def updateTorrentPageFromComicGarden(subscription):
    torrentPage_List = await getTorrentPageFromComicGarden(subscription.index)
    return torrentPage_List[0]

async def update(word_List=None,mode="all"):

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
        subscription_List = subscribe_dir.direct_files
    else:
        subscription_List = subscribe_dir.get_direct_file_byContainMode(word_List,mode=mode)

    async def updateTask(file):

        subscription = deserializeByPickle(file.absolutePath)

        if "index" not in dir(subscription):
            raise DictKeyError("index")

        try:
            torrentPage = await strategy_Dict[subscription.source]['torrentPageStrategy'](subscription)
            subtileGroups = await strategy_Dict[subscription.source]['subtitleGroupStrategy'](torrentPage)
            subtileGroup = [subtitle_group for subtitle_group in subtileGroups if subscription.subtitle_group_name == subtitle_group.name]
            if subtileGroup == []:
                raise ReportError(f"没有匹配目标 目标{subscription.subtitle_group_name} 抓取目标{[subtitle_group.name for subtitle_group in subtileGroups]}")
            torrentGroup = await strategy_Dict[subscription.source]['torrentGroupStrategy'](subtileGroup[0])
            torrentGroup = torrentGroup if subscription.word_List is  None else torrentFilterByKeyword(torrentGroup,subscription.word_List)
            waitDownload(torrentGroup,subscription.download_dir)
        except Exception as e:
            print(f"{e}")
            view_subscription(subscription)
            return None

    tasks = [asyncio.create_task(updateTask(file)) for file in subscription_List]
    await allComplete(tasks)

    try:
        torrentAddition_List = await queueDownload()
        addThread = Thread(target=addTorrentInBatch, args=(qbClient, torrentAddition_List))
        addThread.start()
        addThread.join()
    except Exception as e:
        print(e)


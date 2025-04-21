

from threading import Thread
from api.lib.ToolKits.general.utils import *
from api.lib.ToolKits.request.cfcheck import *
from api.crawlobject import *

async def bthome_update(subscription):
    count = counter()
    return TorrentPage(index = subscription.index, source = "BtHome", title = "更新" , url = subscription.torrent_page_url, htmlText=htmlText)


async def comicgardenupdate(subscription):
    torrentPage_List = await getTorrentPageFromComicGarden(subscription.index)
    return torrentPage_List[0]

async def update(word_List=None,contain_mode="any"):


    subscribe_dir = pathinit(f'{os.path.dirname(sys.argv[0])}/subscribe', make=True, flag="dir")

    if word_List is None:
        subscription_List = subscribe_dir.direct_files
    else:
        subscription_List = subscribe_dir.get_contain_files(word_List,contain_mode=contain_mode)

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
            raise e
            return None

    tasks = [asyncio.create_task(updateTask(file)) for file in subscription_List]
    all_complete(tasks)

    try:
        torrentAddition_List = await queueDownload()
        addThread = Thread(target=addTorrentInBatch, args=(qbClient, torrentAddition_List))
        addThread.start()
        addThread.join()
    except Exception as e:
        raise e
        print(e)


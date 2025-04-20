# 获取异步结果
from api.crawlobject import *
from api.lib.ToolKits.coroutine.coroutineutils import *
from api.lib.torrentcrawl import *
from api.lib.torrentpagecrawl import *
from api.lib.sgcrawl import *
from api.lib.torrentdownload import *
from api.lib.ToolKits.downloadutils.qbtorrentutils import *

qbClient=QbClient(f"{os.path.dirname(sys.argv[0])}/config/config.yaml")

def getTorrentPage(index:Index, stragety=getTorrentPageFromBtHome):
    return async_strategy(stragety(index))

def getSubTitleGroups(torrentPage:TorrentPage, stragety=getSubtitleGroupFromBtHome):
    return async_strategy(stragety(torrentPage))

def getTorrentGroup(subtitleGroup:SubtitleGroup, stragety=getTorrentGroupFromBtHome):
    return async_strategy(stragety(subtitleGroup))

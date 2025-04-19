# 获取异步结果
from api.CrawlObject import *
from api.lib.ToolKits.strategy.AsyncStrategy import *
from api.lib.TorrentCrawl import *
from api.lib.TorrentPageCrawl import *
from api.lib.SubtitleGroupCrawl import *
from api.lib.TorrentDownload import *
from api.lib.ToolKits.downloadutils.qbtorrentutils import *

qbClient=QbClient(f"{os.path.dirname(sys.argv[0])}/config/config.yaml")

def getTorrentPage(index:Index, stragety=getTorrentPageFromBtHome):
    return async_strategy(stragety(index))

def getSubTitleGroups(torrentPage:TorrentPage, stragety=getSubtitleGroupFromBtHome):
    return async_strategy(stragety(torrentPage))

def getTorrentGroup(subtitleGroup:SubtitleGroup, stragety=getTorrentGroupFromBtHome):
    return async_strategy(stragety(subtitleGroup))


from api.CrawlObject import *
from api.lib.ToolKits.Strategy.AsyncStrategy import *
from api.lib.TorrentCrawl import *
from api.lib.TorrentPageCrawl import *
from api.lib.SubtitleGroupCrawl import *
from api.lib.TorrentDownload import *

def getTorrentPage(index:Index, stragety=getTorrentPageFromBtHome):
    return asyncStrategy(stragety(index))

def getSubTitleGroups(torrentPage:TorrentPage, stragety=getSubTitleGroupsFromBtHome):
    return asyncStrategy(stragety(torrentPage))

def getTorrentGroup(subtitleGroup:SubtitleGroup, stragety=getTorrentFromBtHome):
    return asyncStrategy(stragety(subtitleGroup))
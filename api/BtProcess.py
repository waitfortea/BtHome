
from api.CrawlObject import *
from api.lib.ToolKits.Strategy.AsyncStrategy import *
from api.lib.TorrentCrawl import *
from api.lib.TorrentPageCrawl import *
from api.lib.SubtitleGroupCrawl import *
from api.lib.TorrentDownload import *
from api.lib.ToolKits.Download.QbittorrentProcess import *

qbClient=QbClient(f"{os.path.dirname(sys.argv[0])}/config/config.yaml")

def getTorrentPage(index:Index, stragety=getTorrentPageFromBtHome):
    return asyncStrategy(stragety(index))

def getSubTitleGroups(torrentPage:TorrentPage, stragety=getSubtitleGroupFromBtHome):
    return asyncStrategy(stragety(torrentPage))

def getTorrentGroup(subtitleGroup:SubtitleGroup, stragety=getTorrentGroupFromBtHome):
    return asyncStrategy(stragety(subtitleGroup))


from api.lib.ToolKits.Strategy.AsyncStrategy import *
from api.lib.TorrentPageCrawl import *
def getTorrentPage(index,strategy=getTorrentPageFromBtHome):
    asyncStrategy(strategy(index))
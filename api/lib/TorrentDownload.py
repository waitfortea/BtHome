from dataclasses import  dataclass
from api.lib.ToolKits.GeneralObject.StrProcess import *
from api.lib.ToolKits.Proxy import *
from api.CrawlObject import *
@dataclass
class TorrentDownloader:
    pass


def torrentFilterByKeyword(torrentGroup:TorrentGroup,keyWord):
    word_List=keyWord.split(" ")
    result_List=[torrent for torrent in torrentGroup.torrent_List if StrProcessor(torrent.name).contains(word_List,mode='all')]
    return TorrentGroup(torrent_List=result_List,superObj=torrentGroup.superObj)

def torrentDownload():
    pass

def torrentGroupDownload():
    pass

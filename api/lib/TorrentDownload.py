from dataclasses import  dataclass
from api.lib.ToolKits.GeneralObject.StrProcess import *

@dataclass
class TorrentDownloader:
    pass


def torrentFilterByKeyword(torrent_List,keyWord):
    word_List=keyWord.split(" ")
    result_List=[torrent for torrent in torrent_List if StrProcessor(torrent.name).contains(word_List,mode='all')]
    return result_List

def torrentDownload():
    pass

def torrentGroupDownload():
    pass


from api.lib import *
from dataclasses import  dataclass

@dataclass
class TorrentDownloader:
    pass


def torrenFilterByKeyword(keyWord,torrentGroup):
    torrent_List=[]
    word_List=keyWord.split(" ")
    for torrent in torrentGroup.torrent_List:
        if StrProcessor(torrent.name).contains(word_List,mode='all'):
            torrent_List.append(torrent)
    return TorrentGroup(torrent_List=torrent_List,superObj=torrentGroup.superObj)

def torrentDownload():
    pass

def torrentGroupDownload():
    pass

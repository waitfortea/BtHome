from dataclasses import dataclass
from io import BytesIO
from api.lib  import *

@dataclass
class Index():
    keyword:str
    page:str=1
    url:str=None
    title:str=None

    def getTorrentPage(self,stragety):
        return asyncStrategy(stragety(self))

@dataclass
class TorrentPage:
    index: Index
    title: str="TorrentPage"
    url: str=None
    htmlText: str=None

    def getSubTitleGroups(self,stragety):
        return asyncStrategy(stragety(self))

@dataclass
class SubtitleGroup:
    name:str
    superObj:object
    torrentURL_List:list=None
    torrentElement_List:list=None

    def getTorrentGroup(self, stragety):
        return asyncStrategy(stragety(self))
@dataclass
class Torrent:
    name:str
    downloadURL:str

    def addDownloadingQueue(self):
        pass



@dataclass
class TorrentGroup:
    def __init__(self,torrent_List,superObj):
        self.torrent_List=torrent_List
        self.superObj=superObj

    def filter(self,keyword):
        result_List=torrentFilterByKeyword(self.torrent_List,keyword)
        return TorrentGroup(torrent_List=result_List,superObj=self.superObj)


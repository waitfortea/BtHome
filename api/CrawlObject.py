from dataclasses import dataclass
from io import BytesIO
from api.lib.ToolKits.Strategy.AsyncStrategy import *
from api.lib.ToolKits.Proxy import *
from api.lib import *

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
        return  asyncStrategy(stragety(self))

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
    torrent_List:list
    superObj:object

    def filter(self,keyWord):
        return torrenFilterByKeyword(keyWord,self)


if __name__=='__main__':
    setProxy()
    index=Index(keyword="迷宫饭 幻樱字幕组",page=[1,2])
    torrentPage_List=index.getTorrentPage(getTorrentPageFromComicGarden)
    subtitleGroup_List=torrentPage_List[0].getSubTitleGroups(getSubTitleGroupsFromComicGarden)
    torrentGroup=subtitleGroup_List[0].getTorrentGroup(getTorrentFromComicGarden)

    torrentGroup_GB=torrentGroup.filter('GB')
    print(torrentGroup.torrent_List)
    closeSession(aiohttpSession)

__all__="torrentFilterByKeyword",'getTorrentContent','torrentDownload'

from dataclasses import  dataclass
from api.lib.ToolKits.GeneralObject.StrProcess import *
from api.lib.ToolKits.RequestsProcess import *
from api.lib.ToolKits.CustomException import *
from api.lib.ToolKits.CustomType import *
from api.lib.ToolKits.Proxy import *
from api.lib.ToolKits.FileProcess import *
from api.CrawlObject import *
from api.lib.DomainCheck import *
import bencodepy

torrentDownloadingQueue=[]

def torrentFilterByKeyword(torrentGroup:TorrentGroup,keyWord):
    word_List=keyWord.split(" ")
    result_List=[torrent for torrent in torrentGroup.torrent_List if StrProcessor(torrent.name).contains(word_List,mode='all')]
    return TorrentGroup(torrent_List=result_List,superObj=torrentGroup.superObj)

async def getTorrentContent(torrent:Torrent):
        count=0
        while True and count < 10:
            try:
                res=await AsyncRequestsProcessor(domain.address + '/' + torrent.url, proxy=globalProxy.proxy_aiohttp)
                torrentContent_IO = await res.content.read()
                torrentContent = bencodepy.decode(torrentContent_IO)
                break
            except Exception as e:
                print(e)
                count += 1
                print(f'重新获取{count}')
                if count >= 5:
                    callEvent('domainCheck',"")
        return torrentContent

def doEvent_download(torrentGourp):
    global torrentDownloadingQueue
    torrentDownloadingQueue.append(torrentGourp)



class torrentDownloader:
    def __init__(self,downloadPath):
        self.init(downloadPath)
    def init(self,downloadPath):
        self.downloadPath=pathInit(downloadPath).absolutePath
async def torrentDownload():
    async def
        for torrentGroup in torrentDownloadingQueue:


def torrentGroupDownload():
    pass

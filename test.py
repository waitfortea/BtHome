
from api.lib.ToolKits.CustomType import *
from api.lib.ToolKits.Strategy.AsyncStrategy import *
from api.lib.Config import *
from api.lib.TorrentPageCrawl import *
from api.CrawlObject import *
from api.lib.ToolKits.Proxy import *
from api.lib.DomainCheck import *
from api.lib.ToolKits.Event import *
from api.lib.ToolKits.RequestsProcess import *
from api.lib.ToolKits.Download.QbittorrentProcess import *
# print(config)
import os
import aiofiles
setProxy()
async def test():
    content=await AsyncRequestsProcessor("https://dmhy.org/topics/list/page/1",session=aiohttpSession,proxy=globalProxy.proxy_aiohttp,retry=3).text()
    print(content)
    # async with open("test/test.torrent",'wb') as f:
    #     f.write(content)
    # qbClient=QbClient("config/config.yaml")
    # qbClient.addTorrent("test/test.torrent")
asyncStrategy(test())
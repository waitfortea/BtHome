
from api.lib.ToolKits.CustomType import *
from api.lib.ToolKits.Strategy.AsyncStrategy import *
from api.lib.Config import *
from api.lib.TorrentPageCrawl import *
from api.CrawlObject import *
from api.lib.ToolKits.Proxy import *
from api.lib.DomainCheck import *
from api.lib.ToolKits.Event import *
from api.lib.ToolKits.RequestsProcess import *
print(config)
setProxy()
# setup_domainCheck()
# callEvent('domainCheck',"")
# result=asyncStrategy(getTorrentPageFromBtHome(Index("迷宫饭")))
url="https://www.btbtt19.com/search-index-keyword-%E5%A4%9C%E6%99%9A%E6%B0%B4%E6%AF%8D%E4%B8%8D%E4%BC%9A%E6%B8%B8%E6%B3%B3%20%E6%9B%B4%E6%96%B0.htm"
res=RequestsProcessor(url,proxies=globalProxy.proxy_request)
print(res.text())
import asyncio
from api.crawlobject import *
from api.lib.ToolKits.parse.elementutils import *
from api.lib.ToolKits.coroutine.coroutineutils import *
from api.lib.ToolKits.general.strutils import *
from api.lib.ToolKits.general.fileutils import *
from api.lib.ToolKits.request.requestutils import *
from api.lib.config import *

async def getTorrentGroupFromBtHome(subtilegroup):
    torrent_list=[]
    for torrentelement in subtilegroup.torrentelement_List:
        torrentname = FileUtils.verifyfilename(ElementUtils.get_text(torrentelement)).replace("\n","")
        torrenturl= config['source']['bthome']['domain']+"/"+torrentelement.attrib['href']
        torrent = Torrent(name=torrentname, downloadURL=torrenturl,subtitle_group=subtilegroup)
        torrent_list.append(torrent)

    return TorrentGroup(torrent_list=torrent_list, subtitle_group=subtilegroup)


async def getTorrentGroupFromComicGarden(subtitleGroup:SubtitleGroup):
    torrent_list = []
    async def getTorrent(url):
        htmlText=RequestUitls.get_html(name='aiohttp', url="https://dmhy.org"+url, type='get')
        torrent_list=ElementUtils.parse_html(htmlText).xpath("//a[contains(@href,'.torrent')]")
        return torrent_list

    tasks=[asyncio.create_task(getTorrent(url)) for url in subtitleGroup.torrenturl_List]
    result_List=await asyncio.gather(*tasks)
    torrentelement_List=ListUtils.join(result_List)
    for torrentelement in torrentelement_List:
        torrentname=FileUtils.verifyfilename(torrentelement.text())
        downloadURL="https:"+torrentelement.attrib('href')
        torrent_list.append(Torrent(name=torrentname,downloadURL=downloadURL))
    return TorrentGroup(torrent_list=torrent_list,subtitle_group=subtitleGroup)

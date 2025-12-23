import asyncio
from api.crawlobject import *
from api.lib.ToolKits.parse.elementutils import *
from api.lib.ToolKits.coroutine.coroutineutils import *
from api.lib.ToolKits.general.strutils import *
from api.lib.ToolKits.general.fileutils import *
from api.lib.ToolKits.request.requestutils import *
from api.lib.config import *
from api.bthomeutils import *

@BtHomeUtils.register_sourceplugin('bthome_multi_tget')
@BtHomeUtils.register_sourceplugin('bthome_batch_tget')
@BtHomeUtils.register_sourceplugin('bthome_tget')
def bthome_gettorrent(subtilegroup):
    torrent_list=[]
    for torrentelement in subtilegroup.torrentelement_list:
        torrentname = FileUtils.verifyfilename(ElementUtils.get_text(torrentelement)).replace("\n","")
        torrenturl= config['source']['bthome']['domain']+"/"+torrentelement.attrib['href']
        torrent = Torrent(name=torrentname, downloadurl=torrenturl,subtitlegroup=subtilegroup)
        torrent_list.append(torrent)

    return TorrentGroup(torrent_list=torrent_list, subtitlegroup=subtilegroup)


@BtHomeUtils.register_sourceplugin('comicgarden_tget')
def comicgarden_gettorrent(subtitlegroup:SubtitleGroup):
    url_list = [config['source']['comicgarden']['domain'] + url for url in subtitlegroup.torrenturl_list]
    torrent_list = []
    html_list = RequestUitls.get_html(name='dp_multi_tab', type='get', url=url_list)
    torrentele_list=[ElementUtils.parse_html(torrent_html).xpath("//a[contains(@href,'.torrent')]")[0] for torrent_html in html_list]

    for torrentelement in torrentele_list:
        torrentname=FileUtils.verifyfilename(ElementUtils.get_text(torrentelement))
        downloadURL="https:"+torrentelement.attrib['href']
        torrent_list.append(Torrent(name=torrentname,downloadurl=downloadURL,subtitlegroup=subtitlegroup))
    return TorrentGroup(torrent_list=torrent_list, subtitlegroup=subtitlegroup)

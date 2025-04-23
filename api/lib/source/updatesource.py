from api.bthomeutils import *
from api.lib.sql.sqlutils import *
from api.crawlobject import *
import pandas as pd
from api.lib.ToolKits.request.requestutils import *
from api.lib.torrentmanager import *
from api.lib.log import *
from api.bthomeutils import *
from api.lib.ToolKits.parse.elementutils import *
@BtHomeUtils.register_sourceplugin('drissionpage_update')
def bthome_update(mysqlconfig):
    sqlsession = SqlUtils(mysqlconfig, logfun=infolog)
    sqlsession.sql('use bthome')
    sqlsession.sql((
        'select '
        'torrentpage_url, subtitlegroup_id, filterword, savepath, subtitlegroup_name '
        'from subscribe '
        'where in_use = 1'
    ), consolelog=False)
    fetch_dict = sqlsession.fetch(mode='all')
    EventUtils.run('infolog',logdata='返回数据 ' + json.dumps(fetch_dict))
    df = pd.DataFrame(fetch_dict)
    for index, row_series in df.iterrows():
        info_dict = row_series.to_dict()
        htmltext = RequestUitls.get_html(name='drissionpage', type='get', url= info_dict['torrentpage_url'])

        doc = ElementUtils.parse_html(htmltext)
        sgelement_list = doc.xpath('//fieldset[@class="fieldset"][.//a]')
        sgelement = sgelement_list[info_dict['subtitlegroup_id']]
        torrentelement_list = sgelement.xpath('.//a')
        torrent_list = []
        for torrentelement in torrentelement_list:
            torrentname = FileUtils.verifyfilename(ElementUtils.get_text(torrentelement)).replace("\n", "")
            torrenturl = config['source']['bthome']['domain'] + "/" + torrentelement.attrib['href']
            torrent = Torrent(name=torrentname, downloadurl=torrenturl,
                              subtitlegroup=SubtitleGroup(name=info_dict['subtitlegroup_name']
                                                          , torrentpage=TorrentPage(url=info_dict['torrentpage_url'])))
            torrent_list.append(torrent)
        torrent_list = TorrentManager.filtername(torrent_list=torrent_list, word_list=info_dict['filterword'].split(' '))
        torrent_list = TorrentManager.localtorrentcheck(torrent_list=torrent_list, check_path=info_dict['savepath'])
        # if torrent_list:
        torrentpath_list = BtHomeUtils.download_torrent(mode='drissionpage', torrent_list=torrent_list, savepath=info_dict['savepath'])
        BtHomeUtils.qb_add(torrentpath_list=torrentpath_list)



async def comicgardenupdate(subscription):
    pass


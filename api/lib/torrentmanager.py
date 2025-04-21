

import aiofiles
from api.crawlobject import *
from api.lib.ToolKits.general.strutils import *
from api.lib.ToolKits.general.fileutils import *
from api.lib.log import *

class TorrentManager(FileUtils):

    @classmethod
    def filtername(cls, torrent_list, word_list):
        result_list = [torrent for torrent in torrent_list if all(word in torrent.name for word in word_list)]
        result_list = [setattr(torrent,'name', cls.verifyfilename(torrent.name)) for torrent in result_list]
        return result_list

    @classmethod
    def localtorrentcheck(cls, torrent_list, check_path):

        check_dir = cls.pathinit(check_path, flag="dir", make=True)
        checkfile_list = DirUtils.rls(mode='rextension', extension_type_list=['.torrent','.rar'], dir=check_dir)
        checkfilename_set = set([file.basename for file in checkfile_list])

        result_list = [torrent if torrent.name not in checkfilename_set
                       else EventUtils.run(eventname='infolog', logdata=f'忽略种子{torrent.name}')
                       for torrent in torrent_list ]
        return result_list







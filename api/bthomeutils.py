# 获取异步结果
from api.lib.ToolKits.download.qbtorrentutils import *
from api.lib.ToolKits.request.requestutils import *
class BtHomeUtils(QbUtils,RequestUitls):
    __source_plugin = {}
    __torrent_list = []
    __torrentpath_list = []

    @classmethod
    def register_sourceplugin(cls,source):
        def decorator(sourceplugin):
            if cls.__source_plugin.get(source) is None:
                cls.__source_plugin[source] = sourceplugin
                return sourceplugin
        return decorator

    @classmethod
    def search(cls, source, keyword, *args, **kwargs):
        if cls.__source_plugin.get(f'{source}_search') is not None:
            return cls.__source_plugin[f'{source}_search'](keyword, *args, **kwargs)
        else:
            raise ValueError(f"not found source {f'{source}_search'}")

    @classmethod
    def get_subtitlegroup(cls, source, torrentpage, *args, **kwargs):
        if cls.__source_plugin.get(f'{source}_sgget') is not None:
            return cls.__source_plugin[f'{source}_sgget'](torrentpage, *args, **kwargs)
        else:
            raise ValueError(f"not found source {f'{source}_sgget'}")


    @classmethod
    def get_torrent(cls, source, subtitlegroup, *args, **kwargs):
        if cls.__source_plugin.get(f'{source}_tget') is not None:
            return cls.__source_plugin[f'{source}_tget'](subtitlegroup, *args, **kwargs)
        else:
            raise ValueError(f"not found source {f'{source}_tget'}")

    @classmethod
    def add_torrent(cls, torrent_list):
        cls.__torrent_list = torrent_list

    @classmethod
    def clear_torrent(cls):
        cls.__torrent_list.clear()

    @classmethod
    def list_torrent(cls):
        return cls.__torrent_list

    @classmethod
    def download_torrent(cls, savepath):
        for torrent in cls.__torrent_list:
            file_path = cls.save_file(name='drissionpage', url=torrent.downloadurl, filename=torrent.name, savepath=savepath)
            EventUtils.run('infolog', logdata=f'下载完成 字幕组:{torrent.subtitlegroup.name} 源网页:{torrent.subtitlegroup.torrentpage.url} 下载位置:{file_path}')
            cls.__torrentpath_list.append(file_path)

    @classmethod
    def show_torrentpath_list(cls):
        return cls.__torrentpath_list

    @classmethod
    def qb_add(cls, torrentpath_list=None):

        if not cls.checkstatus():
            EventUtils.run('loadqb',config['qbittorrent'])

        cls.addbatchtorrent(cls.__torrentpath_list)


    @classmethod
    def update_torrent(cls):
        pass


    def subscribe(torrentGroup, word_List, download_dir):
        # subscribe_dir = pathinit(f'{os.path.dirname(sys.argv[0])}/subscribe', make=True, flag="dir")
        # subscription = SubtitleSubscription(index=torrentGroup.superObj.superObj.index
        #                                     , torrent_page_url=torrentGroup.superObj.superObj.url
        #                                     , subtitle_group_name=torrentGroup.superObj.name
        #                                     , word_List=word_List
        #                                     , source=torrentGroup.superObj.superObj.source
        #                                     , download_dir=download_dir
        #                                     )
        # serializeByPickle(f'{subscribe_dir.absolutePath}/{torrentGroup.superObj.superObj.index.keyword}.txt',
        #                   subscription)
        pass

from api.lib.source import *
if __name__ == "__main__":
    EventUtils.run('loadconfig')
    EventUtils.run('loadbrowser', path=config['edge_exe_path'])
    torrentpage_list = BtHomeUtils.search(source='bthome', keyword='进击')
    sg = BtHomeUtils.parse_subtitlegroup(source='bthome', torrentpage=torrentpage_list[0])
    print(sg)

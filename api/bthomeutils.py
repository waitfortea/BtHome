# 获取异步结果
from api.lib.ToolKits.download.qbtorrentutils import *
from api.lib.ToolKits.request.requestutils import *
import inspect
class BtHomeUtils(QbUtils,RequestUitls):
    __source_plugin = {}

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
    def download_torrent(cls, mode, savepath, torrent_list, *args, **kwargs):
        if cls.__source_plugin.get(f'{mode}_download') is not None:
            return  cls.__source_plugin[f'{mode}_download'](torrent_list=torrent_list, savepath=savepath, *args, **kwargs)
        else:
            raise ValueError(f"not found source {mode}")


    @classmethod
    def qb_add(cls, torrentpath_list):

        if not cls.checkstatus():
            raise ValueError('qbittorrent disconnected')

        cls.addbatchtorrent(torrentpath_list)

    @classmethod
    def subscribe(cls, source, info_dict, *args, **kwargs):
        if cls.__source_plugin.get(f'{source}_subscribe') is not None:
            return cls.__source_plugin[f'{source}_subscribe'](info_dict=info_dict, *args, **kwargs)
        else:
            raise ValueError(f"not found source {f'{source}_subscribe'}")

    @classmethod
    def update_torrent(cls, mode,  *args, **kwargs):
        if cls.__source_plugin.get(f'{mode}_update') is not None:
            return cls.__source_plugin[f'{mode}_update'](*args, **kwargs)
        else:
            raise ValueError(f"not found source {mode}_update")

class BtHomeUtilsPlugin(RequestUitls):
    @staticmethod
    @BtHomeUtils.register_sourceplugin('drissionpage_download')
    def drissionpagedownload(torrent_list, savepath, *args, **kwargs):
        torrentpath_list = []

        for torrent in torrent_list:
            file_path = RequestUitls.save_file(name='drissionpage', url=torrent.downloadurl, filename=torrent.name,
                                      savepath=savepath)

            EventUtils.run('infolog',
                           logdata=f'下载完成 字幕组:{torrent.subtitlegroup.name} 源网页:{torrent.subtitlegroup.torrentpage.url} 下载位置:{file_path}')
            torrentpath_list.append(file_path)
        return torrentpath_list


from api.lib.source import *
if __name__ == "__main__":
    EventUtils.run('loadconfig')
    EventUtils.run('loadbrowser', path=config['edge_exe_path'])
    torrentpage_list = BtHomeUtils.search(source='bthome', keyword='进击')
    sg = BtHomeUtils.parse_subtitlegroup(source='bthome', torrentpage=torrentpage_list[0])
    print(sg)

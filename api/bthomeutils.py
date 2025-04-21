# 获取异步结果


class BtHomeUtils:
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
    def parse_subtitlegroup(cls, source, torrentpage, *args, **kwargs):
        if cls.__source_plugin.get(f'{source}_sgparse') is not None:
            return cls.__source_plugin[f'{source}_sgparse'](torrentpage, *args, **kwargs)
        else:
            raise ValueError(f"not found source {f'{source}_sgparse'}")

    @classmethod
    def update(cls):
        pass

    @classmethod
    def download(cls):
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

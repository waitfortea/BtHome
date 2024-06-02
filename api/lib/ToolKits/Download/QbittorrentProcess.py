import qbittorrentapi

class QbClient:
    def __init__(self):
        self.qbClient = qbittorrentapi.Client(host='localhost:8087', username='admin', password='a259878')
    def addTorrent(self,TorrentPather):

        try:
            self.qbClient.auth_log_in()
        except qbittorrentapi.LoginFailed as e:
            print(e)
        category = TorrentPather.category# 分类名称
        savePath = TorrentPather.savePath  # 下载路径
        print(f'保存路径为:{savePath}')
        for torrentPath in TorrentPather.torrentPaths_List:
            # 使用API添加种子
            self.qbClient.torrents_add(torrent_files=torrentPath, category=category, savepath=savePath,is_paused=False,
                                    is_sequential_download=True, is_first_last_piece_priority=True)


if __name__=='__main__':
    qbClient = qbittorrentapi.Client(host='localhost:8087', username='admin', password='a259878')
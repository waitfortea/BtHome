import os.path
import sys
from func_timeout import func_set_timeout
import qbittorrentapi
from ..SerializeProcessor import *
from ..FileProcess import *
class QbClient:
    def __init__(self,configPath):
        self.init(configPath)

    def init(self,configPath):
        if isFile(configPath):
            self.configPath=pathInit(configPath).absolutePath
        self.config = YamlProcessor(self.configPath).contentDict

        self.host=self.config['qbittorrent']['host']
        self.username=self.config['qbittorrent']['username']
        self.password=self.config['qbittorrent']['password']
        self.is_paused=self.config['qbittorrent']['is_paused']
        self.is_sequential_download=self.config['qbittorrent']['is_sequential_download']
        self.is_first_last_piece_priority=self.config['qbittorrent']['is_first_last_piece_priority']

        self.qbClient = qbittorrentapi.Client(host=self.host, username=self.username, password=self.password)

    @func_set_timeout(3)
    def checkStatus(self):
        self.qbClient.auth_log_in()


    def addTorrent(self,torrentPath):
        category = os.path.basename(os.path.dirname(torrentPath))# 分类名称
        savePath = rf"{os.path.dirname(torrentPath)}"  # 下载路径
        print(f'保存路径为:{savePath}')
        # 使用API添加种子
        self.qbClient.torrents_add(torrent_files=torrentPath, category=category, savepath=savePath,is_paused=self.is_paused,
                                is_sequential_download=self.is_sequential_download, is_first_last_piece_priority=self.is_first_last_piece_priority)


def addTorrentInBatch(client:QbClient,torrentAddition_List):
    def dfs(path):
        if isFile(path):
            client.addTorrent(path)
            return True
        for torrentPath in path:
            if dfs(torrentPath):
                continue
            else:
                raise Exception
        return True
    print("=========开始添加种子=========")
    dfs(torrentAddition_List)
    print("=========添加种子完毕=========")

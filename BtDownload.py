import asyncio
import aiofiles
import qbittorrentapi
import os
from dataclasses import dataclass
from abc import ABC,abstractmethod
import bencodepy
from ToolKits.FileProcess import PathProcessor
@dataclass
class DownloadPather:
    torrentDom_List:list
    savePath: str

@dataclass
class TorrentPather:
    torrentPaths_List:list
    category:str
    savePath:str

class Downloader(ABC):
    def __init__(self,DownloadClient=None):
        self.DownloadClient=DownloadClient

    @abstractmethod
    def check(self):
        pass

    @abstractmethod
    def download(self):
        pass

class TorrentDowloader(Downloader):

    def check(self,DownloadPather):
        if os.path.isdir(DownloadPather.savePath):
            pass
        else:
            os.makedirs(DownloadPather.savePath,exist_ok=True)
        torrentName_List=[file.fileName for file in PathProcessor.init(DownloadPather.savePath).getFileListBySuffix(['.torrent'])]
        return [torrent for torrent in DownloadPather.torrentDom_List if torrent.name not in torrentName_List]

    def download(self,DownloadPather):
        torrentChecked_List=self.check(DownloadPather)
        torrentPaths_List=[]
        for torrent in torrentChecked_List:
            with open(rf'{DownloadPather.savePath}\{torrent.name}', 'wb') as file:
                torrentPath=f'{DownloadPather.savePath}\\{torrent.name}'
                torrentPaths_List.append(torrentPath)

                file.write(bencodepy.encode(torrent.torrentContent))
                file.close()
        torrentPather=TorrentPather(torrentPaths_List=torrentPaths_List,category=PathProcessor.init(DownloadPather.savePath).dirName,savePath=DownloadPather.savePath)
        return torrentPather

    async def asyncDonwload(self,DownloadPather):
        torrentChecked_List = self.check(DownloadPather)
        DLtasks=[asyncio.create_task(self.asyncDownloadSingleTask(torrent,DownloadPather)) for torrent in torrentChecked_List]
        torrentPaths_List=await asyncio.gather(*DLtasks)
        print(torrentPaths_List)
        torrentPather = TorrentPather(torrentPaths_List=torrentPaths_List, category=PathProcessor.init(DownloadPather.savePath).dirName,
                                      savePath=DownloadPather.savePath)

        return torrentPather

    async def asyncDownloadSingleTask(self,torrent,DownloadPather):

      #由于这里
       async with aiofiles.open(rf'{DownloadPather.savePath}\{torrent.name}', mode='wb') as file:
            torrentPath = f'{DownloadPather.savePath}\\{torrent.name}'
            torrentContent=await torrent.asyncTorrentContent
            await file.write(bencodepy.encode(torrentContent))
       return torrentPath

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
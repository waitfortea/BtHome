
import re
from ToolKits.SerializeProcessor import PickleProcessor
from dataclasses import dataclass
from ToolKits.FileProcess import PathProcessor
import BtDownload
import BtHomeObject as BTO
from ToolKits.GeneralStrategy import AsyncStrategy
import os
from ToolKits.FileProcess import PathProcessor as PP
import Listen
import asyncio
import DomainCheck

@dataclass
class BtSave:
    torrentPageUrl:str
    subtitleGroupOrder:object
    torrentSavePath:str
    comicName:str
    constrainStr_List:list
    subtitleGroupName:str
    def save(self):
        serializationSavePath=rf'H:\app\bt-video\updateLog\{self.comicName}.txt'

        PickleProcessor(savePath=serializationSavePath,obj=self).save()


class BtUpdate:
    def __init__(self,update_List=None):
        if update_List is not None:
            self.update_List=update_List
        else:
            self.update_List=[]

    def append(self,btSave_List):
        self.update_List.extend(btSave_List)

    def clear(self):
        pass
    async def update(self):
        print('------UPDATE START------')
        print('【清空未下载种子】')
        path = PathProcessor.init(r'H:\app\bt-video\2024.4\动漫')
        print(f'检测目录{path}')
        for dir in path.directDirs:
            torrent_List = dir.getFileListBySuffix(['.torrent'])
            # 这里是正则匹配集数,根据集数的差异判断哪些是未下载的
            torrentEpisode_Dict = {re.search('(?<=[\[ ])\d{1,2}(?=[\] ])', torrent.fileName).group(): torrent for
                                   torrent in torrent_List if
                                   re.search('(?<=[\[ ])\d{1,2}(?=[\] ])', torrent.fileName) is not None}
            torrentEpisode_List = [match.group() for match in
                                   map(lambda x: re.search('(?<=[\[ ])\d{1,2}(?=[\] ])', x.fileName), torrent_List) if
                                   match is not None]
            vedio_List = dir.getFileListBySuffix(['.mp4', '.mkv'])
            vedioEpisode_List = [match.group() for match in
                                 map(lambda x: re.search('(?<=[\[ ])\d{1,2}(?=[\] ])', x.fileName), vedio_List) if
                                 match is not None]
            undownloadedEpisodePath_List = [torrentEpisode_Dict[episode] for episode in
                                            list(set(torrentEpisode_List) - set(vedioEpisode_List))]
            if len(undownloadedEpisodePath_List) != 0:
                print(f'未下载集数 {[torrentPath.fileName for torrentPath in undownloadedEpisodePath_List]}')
                [torrentPath.delete() for torrentPath in undownloadedEpisodePath_List]
        print('【已清空未下载种子】')
        parentDir = r'H:\app\bt-video\updateLog'
        filePath_List = [rf'{parentDir}/{file}' for file in os.listdir(parentDir)]
        btSave_List=[]
        for file in [file for file in filePath_List if PP.isFile(file)]:
            btSave = PickleProcessor(savePath=PP.init(file).absolutePath).resotre()
            btSave_List.append(btSave)
        updataTasks=[asyncio.create_task(self.updateTask(btSave)) for btSave in btSave_List]
        results=await asyncio.gather(*updataTasks)
        print('------UPDATE END------')
        await asyncio.sleep(5)
        return results

    async def updateTask(self,btSave):
        while True:
            domain = await DomainCheck.domain_check()
            torrentPageUrl=re.sub('.*\.com',domain,btSave.torrentPageUrl)
            torrentPageDom=BTO.TorrentPage(url=torrentPageUrl)
            subtitleGroupsDom=await torrentPageDom.asyncSubtitleGroups
            break
        subtitleGroupDom=subtitleGroupsDom[btSave.subtitleGroupOrder]
        torrentDom_List=[torrentDom for torrentDom in subtitleGroupDom.torrentsGroup.torrent_List if all(str in torrentDom.name for str in btSave.constrainStr_List)]
        torrentSavaPath=btSave.torrentSavePath
        download_Pather=BtDownload.DownloadPather(torrentDom_List=torrentDom_List,savePath=torrentSavaPath)
        downloader=BtDownload.TorrentDowloader()
        torrentChecked_List=downloader.check(download_Pather)
        if not torrentChecked_List==[]:
            torrent_Pather=await downloader.asyncDonwload(download_Pather)
            try:
                qbClient=BtDownload.QbClient()
            except:
                print('未开启客户端')
            try:
                qbClient.addTorrent(torrent_Pather)
            except:
                print('添加种子失败')

        else:
            print(f"""
【无更新】 保存位置:{torrentSavaPath} 
字幕组:{subtitleGroupDom.name} 网址:{torrentPageUrl} 
已更新集数 {len(torrentDom_List)} 本地集数:{len([file for file in PathProcessor.init(torrentSavaPath).allFiles if file.suffix in ['.mp4','.mkv']])}
            """ )


if __name__=='__main__':
   Listen.setDomainListener()
   AsyncStrategy().execute(BtUpdate().update())


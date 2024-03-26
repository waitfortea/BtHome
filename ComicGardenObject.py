import asyncio
from dataclasses import dataclass
import ToolKits.RequestsProcess as RP
import ToolKits.GeneralStrategy as GS
import ToolKits.Parser as P
import ToolKits.GeneralObject as GO
import numpy as np
import pandas as pd
import bencodepy
import aiohttp
import re
from ToolKits.GeneralStrategy import AsyncStrategy
from typing import *
from ToolKits.Proxy import ProxyProcessor
from ToolKits.DataStructure import ListProcessor

@dataclass
class CGTorrentPage:
    keyWord: str

    async def asyncHtmlText(self,page):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.200',
        }
        params = {
            'keyword': self.keyWord,
        }
        htmlText = await RP.AsyncRequestsProcessor(f'https://dmhy.org/topics/list/page/{page}', params=params, headers=headers,proxy=ProxyProcessor().asyncProxy).text()
        if '服务器遇到错误' in htmlText:
            return None
        else:
            return htmlText

    def htmlText(self,page):
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.200',
        }
        params = {
            'keyword': self.keyWord,
        }
        htmlText = RP.RequestsProcessor(f'https://dmhy.org/topics/list/page/{page}', params=params, headers=headers).text
        if '服务器遇到错误' in htmlText:
            return None
        else:
            return htmlText


    async def asyncSubTitleGroups(self):
        async def getSubtitleGroupsByOnePage(self,page):
            htmlText=await self.asyncHtmlText(page)
            if not htmlText:
                return
            else:
                dom=P.DomParser(P.TextPather(htmlText=htmlText)).dom
                titleElement_List = P.DomParser(P.DomPather(dom=dom, xpath="//td[@class='title']/a")).parse(
                    P.ListElementStrategyByDom())
                title_List = [GO.StrProcessor(title.text).toStrip for title in titleElement_List]

                subtileGroupElement_List = [
                    '其他' if element.xpath('./preceding-sibling::*[1]') == [] else element.xpath('./preceding-sibling::*[1]')[
                        0] for element in titleElement_List]
                subtitleGroupName_List = [GO.StrProcessor(subtitleGroup.text).toStrip if subtitleGroup != '其他' else '其他' for
                                          subtitleGroup in subtileGroupElement_List]
                magnet_List=[ element.xpath("./../..//a[contains( @ href, 'magnet')]")[0].attrib('href') for element in titleElement_List]
                return title_List,subtitleGroupName_List,magnet_List

        tasks = [asyncio.create_task(getSubtitleGroupsByOnePage(self,page+1)) for page in range(20)]
        result_List=await asyncio.gather(*tasks)
        title_List=[]
        subtitleGroupName_List=[]
        magnet_List =[]
        for result in result_List:
            if result:
                title_List+=result[0]
                subtitleGroupName_List+=result[1]
                magnet_List+=result[2]
        subtitleGroup_Dict=ListProcessor(subtitleGroupName_List).converToMatchDict(list(zip(title_List,magnet_List)))
        subtitleGroup_List=[]
        for subTitleGroupName,torrent_List in subtitleGroup_Dict.items():
            torrentGroup=CGTorrentGroup()
            torrent_List = [CGTorrent(name=torrent[0],magnet=torrent[1],parent=torrentGroup) for torrent in torrent_List]
            torrentGroup.torrentGroup=torrent_List
            subTitleGroup= CGSubTitleGroup(name=subTitleGroupName,torrentGroup=torrentGroup,parent=self)
            torrentGroup.parent=subTitleGroup
            subtitleGroup_List.append(subTitleGroup)
        print(subtitleGroup_List)

@dataclass
class CGSubTitleGroup:
    name: str
    torrentGroup: object = None
    parent: object = None

@dataclass
class CGTorrentGroup:
    parent: object = None
    torrentGroup: list  = None

@dataclass
class CGTorrent:
    magnet: str
    name: str
    parent: object  = None



if __name__ == '__main__':
    # print(CGTorrentPage('鬼灭').htmlText(1))
    print(AsyncStrategy().execute(CGTorrentPage('香格里拉').asyncSubTitleGroups())
)

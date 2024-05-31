import asyncio
from dataclasses import dataclass
from  api.lib.ToolKits.RequestsProcess import *
import numpy as np
import pandas as pd
import bencodepy
import aiohttp
import re


@dataclass
class TorrentPage:
    url: str
    title: str = None

    @property
    async def asyncSubtitleGroups(self):
        htmlText = await self.asyncHtmlText
        text_Pather = P.T extPather(htmlText=htmlText, xpath="//td[@class='post_td']//div[@class='message']")
        elements_List = [element for element in P.DomParser(text_Pather).parse(P.ListElementStrategyByText()) if
                         element.xpath('..//a')][1:]
        subtitleGroupName_List = [element.text.replace("\t", "").replace("\n", "").strip() for element in elements_List]
        subtitleGroupDom_Lsit = [element.xpath('..')[0] for element in elements_List]

        extraText_Pather = P.TextPather(htmlText=htmlText, xpath='(//div[@class="attachlist"])[1]')
        extraElement_List = P.DomParser(extraText_Pather).parse(P.ListElementStrategyByText())
        if extraElement_List[0].element.xpath("./preceding-sibling::*[@class='message']") == []:
            extraElement = extraElement_List[0]
            subtitleGroupName_List.insert(0, '主页')
            subtitleGroupDom_Lsit.insert(0, extraElement)

        subtitleGroup_List = []
        if len(subtitleGroupDom_Lsit) == len(subtitleGroupName_List):
            for i in range(len(subtitleGroupDom_Lsit)):
                subtitle_group = SubtitleGroup(name=subtitleGroupName_List[i], dom=subtitleGroupDom_Lsit[i],
                                               superior_Obj=self, order=i)
                subtitleGroup_List.append(subtitle_group)
        return subtitleGroup_List

    async def asyncHtmlText(self,strategy):
        strategy(self)
        count=0
        async with aiohttp.ClientSession() as session:
            while True and count<10:
                try:
                    htmlText = await AsyncRequestsProcessor(self.url,session=session,proxy=proxy_aiohttp).text()
                    return htmlText
                except Exception as e:
                    print(e)
                    count+=1
                    print(f'重新连接{count}')
                    await asyncio.sleep(1)
                    continue


    @property
    def htmlText(self):
        domain = postEvent('getDomain')
        while True:
            try:
                self.url = re.sub('.*\.com', domain, self.url)
                htmlText = RequestsProcessor(self.url,proxies=proxy_request).text()
                return htmlText
            except:
                domain = AsyncStrategy().execute(DomainCheck.domain_check())
                continue




@dataclass
class SubtitleGroup:
    name: str
    dom: str
    order: int
    superior_Obj: object = None

    @property
    def torrentsGroup(self):
        dom_Pather = P.DomPather(dom=self.dom, xpath='.//a[contains(text(),".torrent")]')
        elements_List = P.DomParser(dom_Pather).parse(P.ListElementStrategyByDom())
        torrentNames_List = [element.text for element in elements_List]
        torrentUrls_List = [element.attrib('href') for element in elements_List]
        if self.name == '主页':
            if len(torrentNames_List) == 1:
                torrentNames_List = [name for name in torrentNames_List]
        torrent_List = []
        if len(torrentNames_List) == len(torrentUrls_List):
            for i in range(len(torrentUrls_List)):
                torrent = Torrent(name=torrentNames_List[i], rawUrl=torrentUrls_List[i], superior_Obj=self)
                torrent_List.append(torrent)
        return TorrentGroup(torrent_List=torrent_List, superior_Obj=self)



@dataclass
class TorrentGroup:
    torrent_List: list
    superior_Obj: object = None

    @property
    def num(self):
        pass

    def show(self):
        for torrent in self.torrent_List:
            torrent.show()


@dataclass
class Torrent:
    rawUrl: str
    name: str
    superior_Obj: object = None

    @property
    def torrentContent(self):
        torrentContent_Raw = RequestsProcessor(self.domain + '/' + self.url,proxies=proxy_request).content
        torrentContent = bencodepy.decode(torrentContent_Raw)
        return torrentContent

    @property
    async def asyncTorrentContent(self):
        count=0
        async with aiohttp.ClientSession() as session:
            while True and count<10:
                try:
                    async with session.get(self.domain + '/' + self.url,proxy=proxy_aiohttp) as res:
                        torrentContent_Raw = await res.content.read()
                        torrentContent = bencodepy.decode(torrentContent_Raw)
                        break
                except Exception as e:
                    print(e)
                    count+=1
                    print(f'重新获取{count}')
                    if count>=5:
                        self.domain=await DomainCheck()
                    asyncio.sleep(1)
            await session.close()
            await asyncio.sleep(3)
        print(f'session关闭')
        return torrentContent

    @property
    def url(self):
        return self.rawUrl.replace('dialog', 'download')


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

@dataclass
class SubtitleGroup:
    name: str
    dom: str
    order: int
    superObj: object = None


@dataclass
class TorrentGroup:
    torrent_List: list
    superObj: object = None


@dataclass
class Torrent:
    rawUrl: str
    name: str
    superior_Obj: object = None

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



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





from dataclasses import dataclass
from io import BytesIO
@dataclass
class Index():
    keyword:str
    page:str=None
    url:str=None
    title:str=None

@dataclass
class TorrentPage:
    index: Index
    title: str="TorrentPage"
    url: str=None
    htmlText: str=None

@dataclass
class SubTitleGroup():
    name:str

@dataclass
class TorrentGroup():
    name:str

@dataclass
class Torrent():
    name:str
    content:BytesIO
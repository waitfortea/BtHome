__all__='Index','TorrentPage','SubtitleGroup','TorrentGroup','Torrent','SubtitleSubscription'
from dataclasses import dataclass

@dataclass
class Index:
    """
    url    主站网址
    title  主站名称
    """
    keyword:str
    page:str=1
    url:str=None
    title:str=None

@dataclass
class TorrentPage:
    index: Index
    title: str="TorrentPage"
    url: str=None

@dataclass
class SubtitleGroup:
    name:str
    torrent_page:object
    torrentURL_List:list=None
    torrentElement_List:list=None

@dataclass
class SubtitleSubscription:
    index:object
    torrent_page_url:str
    subtitle_group_name:str
    word_List:list
    download_dir: str
    source:str

@dataclass
class Torrent:
    name:str
    downloadURL:str
    subtitle_group:object

@dataclass
class TorrentGroup:
    torrent_List : list
    subtitle_group : object



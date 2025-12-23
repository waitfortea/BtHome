
from dataclasses import dataclass


@dataclass
class TorrentPage:
    title: str="TorrentPage"
    url: str=None
    htmltext: str=None

@dataclass
class SubtitleGroup:
    name:str
    id:int=None
    torrentpage:object=None
    torrenturl_list:list=None
    torrentelement_list:list=None


@dataclass
class Torrent:
    name:str=None
    downloadurl:str=None
    subtitlegroup:object=None

@dataclass
class TorrentGroup:
    torrent_list : list=None
    subtitlegroup : object=None



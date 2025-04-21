
from dataclasses import dataclass


@dataclass
class TorrentPage:
    title: str="TorrentPage"
    url: str=None

@dataclass
class SubtitleGroup:
    name:str
    torrentpage:object
    torrenturl_list:list=None
    torrentelement_list:list=None


@dataclass
class Torrent:
    name:str
    downloadurl:str
    subtitlegroup:object

@dataclass
class TorrentGroup:
    torrent_list : list
    subtitlegroup : object



# from PyQt5.QtCore import *
# from PyQt5.QtGui import *
# from PyQt5.QtWidgets import *
# from ui.BtHomeStackedWidget import *
#
#
#
# app = QApplication(sys.argv)
# stackedWidget = BtHomeStackedWindow()
# stackedWidget.show()
# sys.exit(app.exec_())
#
from dataclasses import dataclass
from api.lib.DomainCheck import *
from api.lib.ToolKits.Strategy.AsyncStrategy import *
from api.lib.ToolKits.SerializeProcessor import *
from api.lib.ToolKits.RequestsProcess import *
from api.lib.ToolKits.Proxy import *
from api.lib.ToolKits.Event import *
if __name__=='__main__':
    setProxy()
    setup_domainCheck()
    callEvent("domainCheck","")
    closeSession(aiohttpSession)
    # callEvent('domainCheck',"")
    # setProxy()
    # index=Index(keyword="迷宫饭 幻樱字幕组",page=[1,2])
    # torrentPage_List=index.getTorrentPage(getTorrentPageFromComicGarden)
    # subtitleGroup_List=torrentPage_List[0].getSubTitleGroups(getSubTitleGroupsFromComicGarden)
    # torrentGroup=subtitleGroup_List[0].getTorrentGroup(getTorrentFromComicGarden)
    #
    # torrentGroup_GB=torrentGroup.filter('GB')
    #
    # print(torrentGroup_GB.torrent_List)
    # closeSession(aiohttpSession)

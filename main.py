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
from api.BtProcess import *
from api.lib.ToolKits.Proxy import *
from api.lib.Log import *
if __name__=='__main__':

    #设置代理
    setProxy()

    #开启日志
    setup_logNetWork()

    #设置爬虫索引
    index=Index(keyword="迷宫饭 幻樱字幕组",page=[1,2])

    #获取
    torrentPage_List=getTorrentPage(index,getTorrentPageFromComicGarden)

    subtitleGroup_List=getSubTitleGroups(torrentPage_List[0],getSubTitleGroupsFromComicGarden)

    torrentGroup=getTorrentGroup(subtitleGroup_List[0],getTorrentFromComicGarden)

    torrentGroup_GB=torrentFilterByKeyword(torrentGroup,"GB")

    print(torrentGroup_GB.torrent_List)

import sys
from PyQt5.QtCore import QTimer
from PyQt5 import QtWidgets,uic,Qt,sip,QtCore
from PyQt5.QtWidgets import QApplication,QWidget,QLabel,QLineEdit,QCheckBox,QHBoxLayout,QPushButton,QSpacerItem,QScrollArea,QSizePolicy
from PyQt5.QtCore import QThread,pyqtSignal,QObject,pyqtSlot
from qfluentwidgets import FlowLayout
from api.CrawlObject import *
from api.BtProcess import *
from api.lib.Config import *
from api.lib.TorrentDownload import *
import os

class SearchWorker(QObject):

    search = pyqtSignal(object)
    result = pyqtSignal(object)

    @pyqtSlot(object)
    def searchTorrentPage(self,keyword):
        """
            搜索按钮执行的函数，接收索引对象，返回种子页列表对象
        """
        index=Index(keyword=keyword)
        # 获取种子页列表
        torrentPage_List=getTorrentPage(index,getTorrentPageFromBtHome)

        self.result.emit(torrentPage_List)


class TorrentPageWorker(QObject):
    result = pyqtSignal(object )

    @pyqtSlot(object)
    def torrentPageBtnFn(self,torrentPage):
        """
            点击种子页对应按钮执行的函数，接收种子页对象，返回字幕组列表对象
        """

        subtitleGroup_List = getSubTitleGroups(torrentPage,getSubtitleGroupFromBtHome)
        self.result.emit(subtitleGroup_List)

class SubtitleGroupWorker(QObject):
    result = pyqtSignal(object )

    @pyqtSlot(object)
    def subtitleGroupBtn(self,subtitleGroup):
        """
            点击种子页对应按钮执行的函数，接收种子页对象，返回字幕组列表对象
        """

        torrentGroup = getTorrentGroup(subtitleGroup,getTorrentGroupFromBtHome)
        self.result.emit(torrentGroup)



class UpdateWorker(QObject):

    @pyqtSlot()
    def updateBtnFn(self):
        """
        更新追踪种子的函数
        :return:
        """
        pass

class StartWorker(QObject):

    @pyqtSlot(object)
    def startBtnFn(self,window):



        if window.torrentGroup is None:
            return

        torrentGroup=window.torrentGroup

        if window.filterlineEdit.text() is not None:
            word_List = window.filterlineEdit.text().strip().split(" ")
            torrentGroup = torrentFilterByKeyword(torrentGroup,word_List)

        if window.downloadcheckBox.isChecked():
            download_dir = config['download_dir'] if config['download_dir'] is not None else f"{os.path.dirname(__file__)}/../download"
            download_dir = f"{download_dir}/{window.savePathlineEdit.text().strip()}"
            waitDownload(torrentGroup,download_dir)
            # breakpoint()
            try:
                asyncStrategy(queueDownload())
            except Exception as e:
                print(e)
                raise e




class BtWindow(QWidget):

    searchSignal = pyqtSignal(object)
    torrentPageSignal = pyqtSignal(object)
    subtitleGroupSignal = pyqtSignal(object)
    startSignal = pyqtSignal(object)
    updateSignal = pyqtSignal()

    def __init__(self):
        super().__init__()

        # 一个功能的页面配置一个session
        self.searchWorker=SearchWorker()
        self.searchSignal.connect(self.searchWorker.searchTorrentPage)
        self.searchWorker.result.connect(self.getSearchInfo)

        self.torrentPageWorker=TorrentPageWorker()
        self.torrentPageSignal.connect(self.torrentPageWorker.torrentPageBtnFn)
        self.torrentPageWorker.result.connect(self.getSubtitleGroupInfo)

        self.subtitleGroupWorker= SubtitleGroupWorker()
        self.subtitleGroupSignal.connect(self.subtitleGroupWorker.subtitleGroupBtn)
        self.subtitleGroupWorker.result.connect(self.getTorrentGroupInfo)

        self.StartWorker = StartWorker()
        self.startSignal.connect(self.StartWorker.startBtnFn)

        # self.UpdateWorker = UpdateWorker()
        # self.updateSignal.connect(self.UpdateWorker.updateBtnFn)

        self.thread = QThread()
        self.thread.start()
        self.initUI()

    def initUI(self):

        uic.loadUi(rf"{os.path.dirname(__file__)}\..\resource\BtWindowAdvance.ui",self)
        # self.setWindowTitle(f"BTHOME 当前域名为{domain}")
        #绑定按钮
        self.searchBtn.clicked.connect(self.searchBtnFn)
        self.startBtn.clicked.connect(self.startBtnFn)
        self.updateBtn.clicked.connect(self.UpdateBtnFn)
        #设置默认保存位置
        self.savePathlineEdit.setText(config['sub_download_dir'])
        #设置复选框
        self.downloadcheckBox.setChecked(True)
        self.addTorrentcheckBox.setChecked(True)
        self.keepUpdatecheckBox.setChecked(True)

    def searchBtnFn(self):

        self.searchWorker.moveToThread(self.thread)
        self.removeItem(self.torrentPageverticalLayout)
        keyWords = self.searchKeyWordslineEdit.text()
        self.searchSignal.emit(keyWords)

    def getSearchInfo(self,torrentPage_List):
        if torrentPage_List is not None:
            title_List = [torrentPage.title for torrentPage in torrentPage_List]
            for i in range(len(title_List)):
                HLayout = QHBoxLayout()
                HLayout.addWidget(QCheckBox(f"{i + 1}"))
                torrentPageBtn = QPushButton(title_List[i])
                torrentPageBtn.clicked.connect(lambda state,torrePage=torrentPage_List[i]: self.torentPageBtnFn(torrePage))

                HLayout.addWidget(torrentPageBtn)
                HLayout.addStretch()
                self.torrentPageverticalLayout.addLayout(HLayout)
            self.torrentPageverticalLayout.addStretch()

    def torentPageBtnFn(self,torrentPage):
        self.torrentPageWorker.moveToThread(self.thread)
        print('------TORRENTPAGE--------')
        print(torrentPage.title)
        print(torrentPage.url)
        self.removeItem(self.subtitleGroupverticalLayout)
        self.torrentPageSignal.emit(torrentPage)

    def getSubtitleGroupInfo(self,subtitleGroup_List):
        for i in range(len(subtitleGroup_List)):
            subtitleGroupBtn = QPushButton(subtitleGroup_List[i].name)
            HLayout = QHBoxLayout()
            HLayout.addWidget(QCheckBox(f'{i + 1}'))
            HLayout.addWidget(subtitleGroupBtn)
            HLayout.addStretch()
            subtitleGroupBtn.clicked.connect(
                lambda  state,subtitleGroup = subtitleGroup_List[i]: self.subtitleGroupBtnFn(subtitleGroup))
            self.subtitleGroupverticalLayout.addLayout(HLayout)
        self.subtitleGroupverticalLayout.addStretch()
        print('------END--------')

    def subtitleGroupBtnFn(self,subtitleGroup):
        self.subtitleGroupWorker.moveToThread(self.thread)
        print('------SUBTITLEGROUP------')
        print(subtitleGroup.name)
        self.removeItem(self.torrentverticalLayout)
        self.subtitleGroupSignal.emit(subtitleGroup)

    def getTorrentGroupInfo(self,torrentGroup):
        torrent_List = torrentGroup.torrent_List

        for i in range(len(torrent_List)):
            torrentBtn = QPushButton(torrent_List[i].name)
            HLayout = QHBoxLayout()
            HLayout.addWidget(QCheckBox(f'{i + 1}'))
            HLayout.addWidget(torrentBtn)
            HLayout.addStretch()
            # torrentBtn.clicked.connect(lambda  state,torrent = torrent_List[i]: self.torrentBtnFn(torrent))
            self.torrentverticalLayout.addLayout(HLayout)
        self.torrentverticalLayout.addStretch()
        print('------END------')
        self.torrentGroup = torrentGroup

    def torrentBtnFn(self,torrentDom):
        pass

    def removeItem(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.removeItem(item.layout())

    def UpdateBtnFn(self):
        self.UpdateWorker.moveToThread(self.thread)
        self.updateSignal.emit()

    def startBtnFn(self):
        self.StartWorker.moveToThread(self.thread)
        self.startSignal.emit(self)

if __name__=='__main__':
    app = QApplication(sys.argv)
    w=BtWindow()
    w.show()
    app.exec()

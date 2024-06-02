import sys
from PyQt5.QtCore import QTimer
from PyQt5 import QtWidgets,uic,Qt,sip,QtCore
from PyQt5.QtWidgets import QApplication,QWidget,QLabel,QLineEdit,QCheckBox,QHBoxLayout,QPushButton,QSpacerItem,QScrollArea,QSizePolicy
from PyQt5.QtCore import QThread,pyqtSignal,QObject,pyqtSlot
from qfluentwidgets import FlowLayout
import BtDownload as DL



class SearchWorker(QObject):
    """
    
    """

    search = pyqtSignal(str)
    result = pyqtSignal(pd.DataFrame)

    @pyqtSlot(str)
    def searchTorrentPage(self,keyWords):
        index_pather = {
            'keyWords': keyWords
        }
        # 获取索引目录
        torrentPage_DF = CL.IndexCrawler(index_pather).crawler()
        print(torrentPage_DF)
        self.result.emit(torrentPage_DF)


class TorrentPageWorker(QObject):
    result = pyqtSignal(object )

    @pyqtSlot(object)
    def torrentPageBtnFn(self,torrentPageDom):
        subtitleGroup_List = torrentPageDom.subtitleGroups
        self.result.emit(subtitleGroup_List)

class UpdateWorker(QObject):

    @pyqtSlot()
    def updateBtnFn(self):
        AsyncStrategy().execute(BU.BtUpdate().update())

class StartWorker(QObject):

    @pyqtSlot(object)
    def startBtnFn(self,obj):
        constrainStr_List = []
        if obj.filterlineEdit.text():
            constrainStr_List = obj.filterlineEdit.text().strip().split(" ")
            torrentFilter_Pather = FL.FilterPather(dataFrame=obj.torrent_DF, constrainStr_List=constrainStr_List,
                                                   field='torrentName')
            obj.torrentFilterDF = FL.DataFrameFilter(torrentFilter_Pather).filter(FL.StrFilterStrategyByAllInclude())
            print(obj.torrentFilterDF)
        else:
            obj.torrentFilterDF = obj.torrent_DF
            print(obj.torrentFilterDF)
        if obj.downloadcheckBox.isChecked():
            savePath = fr'H:\app\bt-video\{obj.savePathlineEdit.text()}'
            print(savePath)
            if obj.keepUpdatecheckBox.isChecked():
                BU.BtSave(torrentSavePath=savePath, torrentPageUrl=obj.subtitleGroupDom.superior_Obj.url, \
                          subtitleGroupOrder=obj.subtitleGroupDom.order,
                          comicName=savePath.split('\\')[-1], constrainStr_List=constrainStr_List,\
                          subtitleGroupName=obj.subtitleGroupDom.name).save()
            torrentDownload_Pather = DL.DownloadPather(
                torrentDom_List=obj.torrentFilterDF['torrentDom'].to_list()
                , savePath=savePath)
            torrent_Pather = AsyncStrategy().execute(DL.TorrentDowloader().asyncDonwload(torrentDownload_Pather))
            print(torrent_Pather)

        if obj.addTorrentcheckBox.isChecked():
            qBClient = DL.QbClient().addTorrent(torrent_Pather)


class BtWindow(QWidget):
    searchSignal = pyqtSignal(str)
    torrentPageSignal=pyqtSignal(object)
    startSignal=pyqtSignal(object)
    updateSignal=pyqtSignal()

    def __init__(self):
        super().__init__()

        # 一个功能的页面配置一个session
        self.session=aiohttp.ClientSession()

        self.searchWorker=SearchWorker()
        self.searchSignal.connect(self.searchWorker.searchTorrentPage)
        self.searchWorker.result.connect(self.showSearchInfo)

        self.torrentPageWorker=TorrentPageWorker()
        self.torrentPageSignal.connect(self.torrentPageWorker.torrentPageBtnFn)
        self.torrentPageWorker.result.connect(self.showTorrentPageInfo)

        self.StartWorker = StartWorker()
        self.startSignal.connect(self.StartWorker.startBtnFn)

        self.UpdateWorker = UpdateWorker()
        self.updateSignal.connect(self.UpdateWorker.updateBtnFn)

        self.thread = QThread()
        self.thread.start()
        self.initUI()


    def initUI(self):

        uic.loadUi(rf"{PathProcessor.init(__file__).parDir}\BtUI\BtWindowAdvance.ui",self)
        # self.setWindowTitle(f"BTHOME 当前域名为{domain}")
        #绑定按钮
        self.searchBtn.clicked.connect(self.searchBtnFn)
        self.startBtn.clicked.connect(self.startBtnFn)
        self.updateBtn.clicked.connect(self.UpdateBtnFn)
        #设置默认保存位置
        self.savePathlineEdit.setText('2024.1\\')
        #设置复选框
        self.downloadcheckBox.setChecked(True)
        self.addTorrentcheckBox.setChecked(True)
        self.keepUpdatecheckBox.setChecked(True)

    def searchBtnFn(self):

        self.searchWorker.moveToThread(self.thread)
        self.removeItem(self.torrentPageverticalLayout)
        keyWords = self.searchKeyWordslineEdit.text()
        self.searchSignal.emit(keyWords)

    def showSearchInfo(self,torrentPage_DF):
        if not torrentPage_DF.empty:
            title_List = torrentPage_DF['title'].to_list()
            for i in range(len(title_List)):
                HLayout = QHBoxLayout()
                HLayout.addWidget(QCheckBox(f"{i + 1}"))
                torrentPageBtn = QPushButton(title_List[i])
                torrentPageBtn.clicked.connect(
                    lambda state, torrentPageDom=torrentPage_DF.loc[i, 'dom']: self.torentPageBtnFn(torrentPageDom))
                print(torrentPage_DF.loc[i, 'dom'])
                HLayout.addWidget(torrentPageBtn)
                HLayout.addStretch()
                self.torrentPageverticalLayout.addLayout(HLayout)
            self.torrentPageverticalLayout.addStretch()


    def torentPageBtnFn(self,torrentPageDom):
        self.torrentPageWorker.moveToThread(self.thread)
        print('------TORRENTPAGE--------')
        print(torrentPageDom.title)
        print(torrentPageDom.url)
        self.removeItem(self.subtitleGroupverticalLayout)
        self.torrentPageSignal.emit(torrentPageDom)



    def showTorrentPageInfo(self,subtitleGroup_List):
        for i in range(len(subtitleGroup_List)):
            subtitleGroupBtn = QPushButton(subtitleGroup_List[i].name)
            HLayout = QHBoxLayout()
            HLayout.addWidget(QCheckBox(f'{i + 1}'))
            HLayout.addWidget(subtitleGroupBtn)
            HLayout.addStretch()
            subtitleGroupBtn.clicked.connect(
                lambda state, subtitleGroupDom=subtitleGroup_List[i]: self.subtitleGroupBtnFn(subtitleGroupDom))
            self.subtitleGroupverticalLayout.addLayout(HLayout)
        self.subtitleGroupverticalLayout.addStretch()
        print('------END--------')


    def subtitleGroupBtnFn(self,subtitleGroupDom):
        self.subtitleGroupDom = subtitleGroupDom
        print('------SUBTITLEGROUP------')
        print(subtitleGroupDom.name)
        self.removeItem(self.torrentverticalLayout)
        torrentDom_List = subtitleGroupDom.torrentsGroup.torrent_List

        for i in range(len(torrentDom_List)):
            torrentBtn = QPushButton(torrentDom_List[i].name)
            HLayout = QHBoxLayout()
            HLayout.addWidget(QCheckBox(f'{i + 1}'))
            HLayout.addWidget(torrentBtn)
            HLayout.addStretch()
            torrentBtn.clicked.connect(lambda state,torrentDom=torrentDom_List[i]: self.torrentBtnFn(torrentDom))
            self.torrentverticalLayout.addLayout(HLayout)
        self.torrentverticalLayout.addStretch()
        print('------END------')

        torrentName_List=[torrent.name for torrent in torrentDom_List]
        torrentDict={
            'torrentName':torrentName_List
            ,'torrentDom':torrentDom_List
        }
        self.torrent_DF=pd.DataFrame(torrentDict)

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
    pd.set_option('display.max_colwidth', None)  # 显示所有列，不进行缩略

    # 加载监听器
    Listen.setLogListener()
    Listen.setDomainListener()


    app = QApplication(sys.argv)
    w=BtWindow()
    w.show()
    app.exec()

    #
    # #执行BtHome爬虫任务
    # AsyncStrategy().execute(asyncBtHomeCrawlMain())



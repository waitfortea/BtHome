from PyQt5 import uic
from PyQt5.QtWidgets import QApplication,QWidget, QCheckBox,QHBoxLayout,QPushButton
from PyQt5.QtCore import QThread,pyqtSignal,QObject,pyqtSlot
import os
from threading import Thread

from api.lib.ToolKits.download.qbtorrentutils import *
from api.lib.ToolKits.parse.generalutils import *
from api.lib.source.sgsubcribe import *
from api.lib.config import *
from api.lib.torrentdownload import *
from api.bthomeutils import *


class SearchClickWorker(QObject):

    search = pyqtSignal(object)
    result = pyqtSignal(object)

    @pyqtSlot(object,object)
    def search(self,searchlinetext, sourceid):
        """
            搜索按钮执行的函数，接收索引对象，返回种子页列表对象

        """
        # word=searchlinetext.split(";")[0]
        # page=re.search("\d+-\d+", searchlinetext)
        # page_list=pageParser(page.group()) if page is not None else 1

        # 获取种子页列表
        torrentpage_list=BtHomeUtils.search(source=config['sourceid'][sourceid], keyword=searchlinetext)

        self.result.emit(torrentpage_list)


class TorrentPageClickWorker(QObject):
    result = pyqtSignal(object)

    @pyqtSlot(object,object)
    def parse_subtitlegroup(self,torrentpage,sourceid):
        """
            点击种子页对应按钮执行的函数，接收种子页对象，返回字幕组列表对象
        """

        subtitlegroup_list = BtHomeUtils.parse_subtitlegroup(source=config['sourceid'][sourceid], torrentpage=torrentpage)
        self.result.emit(subtitlegroup_list)

class SubtitleGroupClickWorker(QObject):
    result = pyqtSignal(object)

    @pyqtSlot(object,object)
    def subtitlegroupBtn(self,subtitlegroup,sourceid):
        """
            点击种子页对应按钮执行的函数，接收种子页对象，返回字幕组列表对象
        """

        torrentGroup = getTorrentGroup(subtitlegroup,sourceid)
        self.result.emit(torrentGroup)



class UpdateClickWorker(QObject):

    @pyqtSlot()
    def update(self):
        """
        更新追踪种子的函数
        :return:
        """
        pass 

class StartClickWorker(QObject):

    @pyqtSlot(object)
    def startclick(self,window):

        if window.torrentGroup is None:
            return

        torrentGroup=window.torrentGroup

        if window.filterlineEdit.text() is not None:
            word_list = window.filterlineEdit.text().strip().split(" ")
            torrentGroup = torrentFilterByKeyword(torrentGroup,word_list)
        else:
            word_list = None

        download_dir = config['download_dir'] if config[
                                                     'download_dir'] is not None else f"{os.path.dirname(sys.argv[0])}/download"
        download_dir = f"{download_dir}/{window.savePathlineEdit.text().strip()}"

        if window.downloadcheckBox.isChecked():
            torrent_group_add(torrentGroup,pathinit(download_dir,flag='dir',make=True).absolutePath)

            try:
                torrent_path_list=queueDownload()
                if window.addTorrentcheckBox.isChecked():
                    addThread=Thread(target=addTorrentInBatch,args=(qbClient,torrent_path_list))
                    addThread.start()
                    addThread.join()
            except Exception as e:
                print(e)
                raise e

        # if window.keepUpdatecheckBox.isChecked():
        #     subscribe(torrentGroup,word_list,download_dir)

class BtWindow(QWidget):

    #设置ui信号
    search_signal = pyqtSignal(object,object)
    torrentpage_signal = pyqtSignal(object,object)
    sg_signal = pyqtSignal(object,object)
    start_signal = pyqtSignal(object)
    update_signal = pyqtSignal()

    def __init__(self):
        super().__init__()

        #点击搜索
        self.searchclick_work=SearchClickWorker()
        self.search_signal.connect(self.searchclick_work.search)
        self.searchclick_work.result.connect(self.searchclick_callback)

        #点击torrentpage
        self.torrentpageclick_worker=TorrentPageClickWorker()
        self.torrentpage_signal.connect(self.torrentpageclick_worker.parse_subtitlegroup)
        self.torrentpageclick_worker.result.connect(self.torentpageclick_callback)

        #点击subtitlegroup
        self.sgclick_worker= SubtitleGroupClickWorker()
        self.sg_signal.connect(self.sgclick_worker.subtitlegroupBtn)
        self.sgclick_worker.result.connect(self.sgclick_callback)

        #点击start
        self.startclick_worker = StartClickWorker()
        self.start_signal.connect(self.startclick_worker.startclick)

        # 点击update
        self.updateclick_worker = UpdateClickWorker()
        self.update_signal.connect(self.updateclick_worker.update)

        # 点击start
        self.thread = QThread()
        self.thread.start()
        self.initui()



    def initui(self):

        uic.loadUi(rf"{os.path.dirname(sys.argv[0])}\resource\BtWindowAdvance.ui",self)

        # self.setWindowTitle(f"BTHOME 当前域名为{domain}")
        
        #绑定按钮
        self.searchBtn.clicked.connect(self.searchclick)
        self.startBtn.clicked.connect(self.startclick)
        self.updateBtn.clicked.connect(self.updateclick)
        
        #设置默认保存位置
        self.savePathlineEdit.setText(config['sub_download_dir'])
        
        #设置复选框
        self.downloadcheckBox.setChecked(True)
        self.addTorrentcheckBox.setChecked(True)
        self.keepUpdatecheckBox.setChecked(False)

        self.crawlSourceComboBox.currentIndex = 0
        self.crawlSourceComboBox.currentIndexChanged.connect(self.changeCrawlSource)


        self.proxyCheckBox.checked = False
        self.proxyCheckBox.toggled.connect(self.proxCheck)

    def changeCrawlSource(self,index):
        self.crawlSourceComboBox.currentIndex=index
        print(f"更改爬虫源为{self.crawlSourceComboBox.currentIndex}")

    def proxCheck(self,checked):
        pass
        # if checked:
        #     print("开启代理")
        #     setProxy()
        # else:
        #     unsetProxy()
        #     print("关闭代理")


    def searchclick(self):
        print("===========开始搜索==============")
        self.searchclick_work.moveToThread(self.thread)
        self.removeitem(self.torrentPageverticalLayout)
        searchlinetext = self.searchKeyWordslineEdit.text()
        self.search_signal.emit(searchlinetext,self.crawlSourceComboBox.currentIndex)

    def searchclick_callback(self,torrentpage_list):
        if torrentpage_list !=[]:
            title_list = [torrentpage.title for torrentpage in torrentpage_list]
            print("\n".join(title_list))
            for i in range(len(title_list)):
                HLayout = QHBoxLayout()
                HLayout.addWidget(QCheckBox(f"{i + 1}"))
                torrentpageBtn = QPushButton(title_list[i])
                torrentpageBtn.clicked.connect(lambda state,torrePage=torrentpage_list[i]: self.torentpageclick(torrePage))

                HLayout.addWidget(torrentpageBtn)
                HLayout.addStretch()
                self.torrentPageverticalLayout.addLayout(HLayout)
            self.torrentPageverticalLayout.addStretch()
        else:
            print("搜索结果为空")
        print("===========结束搜索==============")

    def torentpageclick(self,torrentpage):
        self.torrentpageclick_worker.moveToThread(self.thread)
        print('------TORRENTPAGE--------')
        print(torrentpage.title)
        print(torrentpage.url)
        self.removeitem(self.subtitleGroupverticalLayout)
        self.torrentpage_signal.emit(torrentpage,self.crawlSourceComboBox.currentIndex)
        print("===========搜索结束==============")

    def torentpageclick_callback(self, subtitlegroup_list):
        for i in range(len(subtitlegroup_list)):
            subtitlegroupBtn = QPushButton(subtitlegroup_list[i].name)
            HLayout = QHBoxLayout()
            HLayout.addWidget(QCheckBox(f'{i + 1}'))
            HLayout.addWidget(subtitlegroupBtn)
            HLayout.addStretch()
            subtitlegroupBtn.clicked.connect(
                lambda state, subtitlegroup=subtitlegroup_list[i]: self.sgclick(subtitlegroup))
            self.subtitleGroupverticalLayout.addLayout(HLayout)
        self.subtitleGroupverticalLayout.addStretch()
        print('------END--------')

    def sgclick(self,subtitlegroup):
        self.sgclick_worker.moveToThread(self.thread)
        print('------SUBTITLEGROUP------')
        print(subtitlegroup.name)
        self.removeitem(self.torrentverticalLayout)
        self.sg_signal.emit(subtitlegroup,self.sourceid)



    def sgclick_callback(self,torrentGroup):
        torrent_list = torrentGroup.torrent_list

        for i in range(len(torrent_list)):
            torrentBtn = QPushButton(torrent_list[i].name)
            HLayout = QHBoxLayout()
            HLayout.addWidget(QCheckBox(f'{i + 1}'))
            HLayout.addWidget(torrentBtn)
            HLayout.addStretch()
            # torrentBtn.clicked.connect(lambda  state,torrent = torrent_list[i]: self.torrentclick(torrent))
            self.torrentverticalLayout.addLayout(HLayout)
        self.torrentverticalLayout.addStretch()
        print('------END------')
        self.torrentGroup = torrentGroup

    def torrentclick(self,torrentDom):
        pass

    def removeitem(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.removeitem(item.layout())

    def updateclick(self):
        self.updateclick_worker.moveToThread(self.thread)
        self.update_signal.emit()

    def startclick(self):
        self.startclick_worker.moveToThread(self.thread)
        self.start_signal.emit(self)

if __name__=='__main__':
    app = QApplication(sys.argv)
    w=BtWindow()
    w.show()
    app.exec()

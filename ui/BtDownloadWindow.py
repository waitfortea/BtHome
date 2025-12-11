from PyQt5 import uic
from PyQt5.QtWidgets import QApplication,QWidget, QCheckBox,QHBoxLayout,QPushButton
from PyQt5.QtCore import QThread,pyqtSignal,QObject,pyqtSlot
import os
from threading import Thread

from api.lib.ToolKits.download.qbtorrentutils import *
from api.lib.ToolKits.parse.generalutils import *
from api.lib.source.sgsubcribe import *
from api.lib.config import *
from api.lib.ToolKits.general.datetimeutils import *
from api.lib.torrentmanager import *
from api.bthomeutils import *


class SearchClickWorker(QObject):

    # search = pyqtSignal(object)
    result = pyqtSignal(object)

    @pyqtSlot(object,object,object)
    def search(self,searchlinetext, sourceid, page_range):
        """
            搜索按钮执行的函数，接收索引对象，返回种子页列表对象

        """
        # word=searchlinetext.split(";")[0]
        # page=re.search("\d+-\d+", searchlinetext)
        # page_list=pageParser(page.group()) if page is not None else 1

        # 获取种子页列表
        torrentpage_list=BtHomeUtils.search(source=config['sourceid'][sourceid], keyword=searchlinetext, page_range = page_range)

        self.result.emit(torrentpage_list)


class TorrentPageClickWorker(QObject):
    result = pyqtSignal(object)

    @pyqtSlot(object,object)
    def parse_subtitlegroup(self,torrentpage,sourceid):
        """
            点击种子页对应按钮执行的函数，接收种子页对象，返回字幕组列表对象
        """

        subtitlegroup_list = BtHomeUtils.get_subtitlegroup(source=config['sourceid'][sourceid], torrentpage=torrentpage)
        self.result.emit(subtitlegroup_list)

class BatchGetTorrentClickWorker(QObject):
    result = pyqtSignal(object)

    @pyqtSlot(object, object)
    def parse_torrentpage_list(self, torrentpage_list, sourceid):
        """
            点击种子页对应按钮执行的函数，接收种子页对象，返回字幕组列表对象
        """

        subtitlegroup_list = BtHomeUtils.get_subtitlegroup(source=config['sourceid'][sourceid], torrentpage=torrentpage_list)
        self.result.emit(subtitlegroup_list)

class SubtitleGroupClickWorker(QObject):
    result = pyqtSignal(object)

    @pyqtSlot(object,object)
    def subtitlegroupBtn(self,subtitlegroup,sourceid):
        """
            点击种子页对应按钮执行的函数，接收种子页对象，返回字幕组列表对象
        """

        torrentgroup = BtHomeUtils.get_torrent(source=config['sourceid'][sourceid], subtitlegroup=subtitlegroup)
        self.result.emit(torrentgroup)


class UpdateClickWorker(QObject):

    @pyqtSlot()
    def update(self):
        """
        更新追踪种子的函数
        :return:
        """
        BtHomeUtils.update_torrent(mode='drissionpage', mysqlconfig=config['mysql'])

class StartClickWorker(QObject):

    @pyqtSlot(object,object)
    def startclick(self, window, source_id):

        if window.current_torrentgroup is None:
            return

        download_dir = config['download_dir'] if config[
            'download_dir'] else f"{os.path.dirname(sys.argv[0])}/download"
        download_dir = f"{download_dir}/{window.savePathlineEdit.text().strip()}"
        download_dir = FileUtils.pathinit(download_dir, flag='dir', make=True).absolutepath

        torrent_list = window.current_torrentgroup.torrent_list

        if window.filterlineEdit.text() is not None:
            word_list = window.filterlineEdit.text().strip().split(" ")
            torrent_list = TorrentManager.filtername(torrent_list, word_list)
            torrent_list = TorrentManager.localtorrentcheck(torrent_list, download_dir)

        if window.downloadcheckBox.isChecked():
            torrentpath_list = BtHomeUtils.download_torrent(mode='drissionpage', torrent_list=torrent_list, savepath=download_dir)

        if window.addTorrentcheckBox.isChecked():
            addThread=Thread(target=BtHomeUtils.qb_add, args=(torrentpath_list,))
            addThread.start()
            addThread.join()

        if window.keepUpdatecheckBox.isChecked():
            torrentgroup = window.current_torrentgroup

            info_dict = {
                'torrentpage_url':torrentgroup.subtitlegroup.torrentpage.url,
                'subtitlegroup_name':torrentgroup.subtitlegroup.name,
                'subtitlegroup_id':torrentgroup.subtitlegroup.id,
                'filterword':window.filterlineEdit.text(),
                'savepath':download_dir
            }
            BtHomeUtils.subscribe(source='bthome', info_dict=info_dict, mysqlconfig=config['mysql'])

class BtWindow(QWidget):

    #设置ui信号
    search_signal = pyqtSignal(object,object,object)
    torrentpage_signal = pyqtSignal(object,object)
    sg_signal = pyqtSignal(object,object)
    batchtorrent_signal = pyqtSignal(object,object)
    start_signal = pyqtSignal(object, object)
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

        #点击批处理
        self.batch_gettorrent_click_worker = BatchGetTorrentClickWorker()
        self.batchtorrent_signal.connect(self.batch_gettorrent_click_worker.parse_torrentpage_list)
        self.batch_gettorrent_click_worker.result.connect(self.sgclick_callback)
        self.batchGetTorrentpushButton.clicked.connect(lambda state, torrePage=torrentpage_list[i]: self.torentpageclick(torrePage))


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

        if config['seasonal_mode']:
            current_month = DatetimeUtils.to_now().month
            month = [i for i in [1,4,7,10] if 0<=current_month-i<3][0]
        self.savePathlineEdit.setText(f'{DatetimeUtils.to_now().replace(month=month).strftime("%Y.%m")}/'+config['sub_download_dir'])
        
        #设置复选框
        self.downloadcheckBox.setChecked(True)
        self.addTorrentcheckBox.setChecked(True)
        self.keepUpdatecheckBox.setChecked(False)

        self.crawlSourceComboBox.currentIndex = 0
        self.crawlSourceComboBox.currentIndexChanged.connect(self.changeCrawlSource)


        self.proxyCheckBox.checked = False
        self.proxyCheckBox.toggled.connect(self.proxCheck)


        #管理 BTHOME OBJECT
        self.global_torrentpage_list = []
        self.global_subtitlegroup_list = []
        # self.global_torrentpage
        # 测试
        self.searchKeyWordslineEdit.setText("喜人奇妙夜2")
        self.pageRangelineEdit.setText('5')

    def changeCrawlSource(self,index):
        self.crawlSourceComboBox.currentIndex=index
        EventUtils.run('infolog', f"更改爬虫源为{self.crawlSourceComboBox.currentIndex}")


    def proxCheck(self,checked):
        pass


    def searchclick(self):
        self.searchclick_work.moveToThread(self.thread)
        self.removeitem(self.torrentPageverticalLayout)
        searchlinetext = self.searchKeyWordslineEdit.text()
        pagerangelinetext = self.pageRangelineEdit.text()
        self.search_signal.emit(searchlinetext,self.crawlSourceComboBox.currentIndex, int(pagerangelinetext))

    def searchclick_callback(self,torrentpage_list):
        self.global_torrentpage_list = torrentpage_list
        if torrentpage_list:
            title_list = [torrentpage.title for torrentpage in torrentpage_list]
            for i in range(len(title_list)):
                HLayout = QHBoxLayout()
                HLayout.addWidget(QCheckBox(f"{i + 1}"))
                torrentpageBtn = QPushButton(title_list[i])
                torrentpageBtn.clicked.connect(lambda state,torrePage=torrentpage_list[i]: self.torentpageclick(torrePage))
                #绑定每个新生成的种子页按纽的点击函数

                HLayout.addWidget(torrentpageBtn)
                HLayout.addStretch()
                self.torrentPageverticalLayout.addLayout(HLayout)
            self.torrentPageverticalLayout.addStretch()


    def torentpageclick(self):
        self.batch_gettorrent_click_worker.moveToThread(self.thread)
        EventUtils.run('infolog', 'batch_click')
        self.removeitem(self.subtitleGroupverticalLayout)
        self.batchtorrent_signal.emit(self.global_torrentpage_list,self.crawlSourceComboBox.currentIndex)

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

    def batch_gettorrent_click(self, torrentpage):
        self.torrentpageclick_worker.moveToThread(self.thread)
        EventUtils.run('infolog', " ".join(['click', torrentpage.title, torrentpage.url]))
        self.removeitem(self.subtitleGroupverticalLayout)
        self.torrentpage_signal.emit(torrentpage, self.crawlSourceComboBox.currentIndex)

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


    def sgclick(self,subtitlegroup):
        self.sgclick_worker.moveToThread(self.thread)
        EventUtils.run('infolog', " ".join(['click', subtitlegroup.name]))
        self.removeitem(self.torrentverticalLayout)
        self.sg_signal.emit(subtitlegroup,self.crawlSourceComboBox.currentIndex)



    def sgclick_callback(self,torrentgroup):
        torrent_list = torrentgroup.torrent_list

        for i in range(len(torrent_list)):
            torrentBtn = QPushButton(torrent_list[i].name)
            HLayout = QHBoxLayout()
            HLayout.addWidget(QCheckBox(f'{i + 1}'))
            HLayout.addWidget(torrentBtn)
            HLayout.addStretch()
            # torrentBtn.clicked.connect(lambda  state,torrent = torrent_list[i]: self.torrentclick(torrent))
            self.torrentverticalLayout.addLayout(HLayout)
        self.torrentverticalLayout.addStretch()
        self.current_torrentgroup = torrentgroup

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
        self.start_signal.emit(self, self.crawlSourceComboBox.currentIndex)

if __name__=='__main__':
    app = QApplication(sys.argv)
    w=BtWindow()
    w.show()
    app.exec()

import pandas as pd
import sys
sys.path.append("..") # 将父目录放入系统路径中,不需要再base_dir中增加__init__.py脚本。
# 备注：sys.path.append中的内容也可以是module1.py 所在文件夹的全局路径
import Listen
import Crawler as CL
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets,uic,Qt,sip,QtCore
from  ToolKits.GeneralStrategy import AsyncStrategy
import random

class SeasonalCrawlWorker(QObject):
    result=pyqtSignal(object)

    @pyqtSlot()
    def seasonalCrawl(self):
        seasonalComic_DF=AsyncStrategy().execute(CL.seasonalComicCrawl().asyncCrawler())
        print('------番剧时间表 END------')
        self.result.emit(seasonalComic_DF)

class SeasonalComincWindow(QWidget):

    seasonalCrawlSignal=pyqtSignal()

    def __init__(self):
        super().__init__()
        self.seasonalComic_List = []
        self.thread=QThread()
        self.thread.start()

        self.SeasonalCrawlWorker=SeasonalCrawlWorker()
        self.seasonalCrawlSignal.connect(self.SeasonalCrawlWorker.seasonalCrawl)
        self.SeasonalCrawlWorker.result.connect(self.initUI)

        self.SeasonalCrawlWorker.moveToThread(self.thread)
        self.seasonalCrawlSignal.emit()

    def initUI(self,seasonalComic_DF):

        self.seasonalComic_DF=seasonalComic_DF

        for i in range(5):
            self.seasonalComic_List.extend(self.seasonalComic_DF.iloc[i,1].values.flatten().tolist())
        self.seasonalComic_List=[comic for comic in self.seasonalComic_List if not pd.isna(comic)]
        VLayout = QVBoxLayout()
        self.setLayout(VLayout)
        self.stackedLayout=QStackedLayout()
        VLayout.addLayout(self.stackedLayout)

        switchButton=QPushButton('Switch')
        switchButton.clicked.connect(self.switchButtonFn)
        VLayout.addWidget(switchButton)


        for i in range(5):
            showWidget=QWidget()
            layout=QVBoxLayout(showWidget)
            layout.addWidget(QLabel(self.seasonalComic_DF.iloc[i, 0]))

            seasonalGirdLayout = QGridLayout()
            layout.addLayout(seasonalGirdLayout)

            singalSeasonalComic_DF=self.seasonalComic_DF.iloc[i,1]
            index_List=singalSeasonalComic_DF.index.tolist()
            columns_List=singalSeasonalComic_DF.columns.tolist()

            for i in range(len(singalSeasonalComic_DF.index)):
                for j in range(len(singalSeasonalComic_DF.iloc[i])):
                    seasonalGirdLayout.addWidget(QLabel(str(index_List[i])), i+1, 0)
                    seasonalGirdLayout.addWidget(QLabel(str(columns_List[j])), 0, j+1)
                    seasonalGirdLayout.addWidget(QLabel(str(singalSeasonalComic_DF.iloc[i,j])),i+1,j+1)

            self.stackedLayout.addWidget(showWidget)

    def switchButtonFn(self):
        index=random.randint(0,4)
        print(index)
        self.stackedLayout.setCurrentIndex(index)


if __name__=='__main__':
    Listen.setDomainListener()
    pd.set_option('display.max_colwidth', None)  # 显示所有列，不进行缩略
    app = QApplication(sys.argv)
    w = SeasonalComincWindow()
    w.show()
    app.exec()



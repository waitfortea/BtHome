import os.path

from BtDownloadWindow import BtWindow
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets,uic,Qt,sip,QtCore
from SeasonalComicWindow import SeasonalComincWindow
import Listen
import BtML
from ToolKits.FileProcess import PathProcessor
class BtHomeStackedWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        uic.loadUi(rf"{PathProcessor.init(__file__).parDir}\BtUI\BtHomeStackedWidget.ui", self)

        self.btHomeStackedLayout=QStackedLayout()
        self.btHomeStackedwidget.setLayout(self.btHomeStackedLayout)


        self.downloadPage=BtWindow()
        self.btHomeStackedLayout.addWidget(self.downloadPage)
        self.seasonalTimeTable = SeasonalComincWindow()


        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        scroll_area = QScrollArea(central_widget)

        scroll_area.setWidget(self.seasonalTimeTable)
        scroll_area.setWidgetResizable(True)

        layout.addWidget(scroll_area)

        self.btHomeStackedLayout.addWidget(central_widget)

        self.timeTablepushButton.clicked.connect(self.timeTablePushButtonFn)

        self.downloadPagepushButton.clicked.connect(self.downloadPagePushButtonFn)

        self.autoNamepushButton.clicked.connect(self.autoNameButtonFn)


    def autoNameButtonFn(self):
        if self.seasonalTimeTable.seasonalComic_List:
            print('------AUTONAME------')
            text=self.downloadPage.searchKeyWordslineEdit.text()
            targetText=BtML.getMaxSimilarityText(text,self.seasonalTimeTable.seasonalComic_List)[0][1]
            saveText=self.downloadPage.savePathlineEdit.text()
            print(f'【匹配结果】 {targetText} \n【保存路径】 {saveText}')
            print('------END------')
            self.downloadPage.savePathlineEdit.setText(saveText+targetText)
        else:
            pass


    def downloadPagePushButtonFn(self):
        self.btHomeStackedLayout.setCurrentIndex(0)

    def timeTablePushButtonFn(self):
        self.btHomeStackedLayout.setCurrentIndex(1)


if __name__ == '__main__':
    Listen.setDomainListener()
    app = QApplication(sys.argv)
    stackedWidget = BtHomeStackedWindow()
    stackedWidget.show()
    sys.exit(app.exec_())




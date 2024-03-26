import sys
import BtHomeStackedWidget as BS
import Listen
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *



Listen.setDomainListener()
app = QApplication(sys.argv)
stackedWidget = BS.BtHomeStackedWindow()
stackedWidget.show()
sys.exit(app.exec_())



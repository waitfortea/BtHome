from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from ui.BtHomeStackedWidget import *



app = QApplication(sys.argv)
stackedWidget = BtHomeStackedWindow()
stackedWidget.show()
sys.exit(app.exec_())



from ui.BtDownloadWindow import *
from api.lib.log import *
from api.lib.cfcheck import *



if __name__=='__main__':

    #设置代理
    # setProxy()

    #开启日志
    setup_log()
    # setup_domainCheck()
    # setup_cfcheck()

    app = QApplication(sys.argv)
    stackedWidget = BtWindow()
    stackedWidget.show()
    sys.exit(app.exec_())

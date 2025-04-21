from ui.BtDownloadWindow import *
from api.lib.config import *

if __name__=='__main__':

    #设置代理
    # setProxy()

    #开启日志
    EventUtils.seton('downloadlog')
    EventUtils.seton('networklog')
    EventUtils.run('loadconfig')
    EventUtils.run(eventname='loadbrowser', path=config['edge_exe_path'])

    app = QApplication(sys.argv)
    stackedWidget = BtWindow()
    stackedWidget.show()
    sys.exit(app.exec_())


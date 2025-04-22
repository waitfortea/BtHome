from ui.BtDownloadWindow import *
from api.lib.config import *

if __name__=='__main__':

    #设置代理
    # setProxy()

    #开启
    EventUtils.seton('downloadlog')
    EventUtils.seton('networklog')
    EventUtils.seton('infolog')
    EventUtils.seton('loadconfig')
    EventUtils.seton('loadbrowser')
    EventUtils.seton('loadqb')

    EventUtils.run('loadconfig')
    EventUtils.run('loadqb',config['qbittorrent'])
    EventUtils.run(eventname='loadbrowser', path=config['edge_exe_path'])

    app = QApplication(sys.argv)
    stackedWidget = BtWindow()
    stackedWidget.show()
    sys.exit(app.exec_())


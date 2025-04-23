from ui.BtDownloadWindow import *
from api.lib.config import *

if __name__=='__main__':

    #设置代理
    # setProxy()

    #开启
    EventUtils.seton('downloadlog')
    EventUtils.seton('networklog')
    EventUtils.seton('infolog')

    config.loadconfig(rf'{os.path.dirname(sys.argv[0])}\config\config.yaml')
    EventUtils.frun('loadqb', config['qbittorrent'], infolog)
    EventUtils.frun(eventname='loadbrowser', path=config['edge_exe_path'])

    app = QApplication(sys.argv)
    stackedWidget = BtWindow()
    stackedWidget.show()
    sys.exit(app.exec_())


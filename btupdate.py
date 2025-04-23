from ui.BtDownloadWindow import *
from api.lib.config import *
from api.bthomeutils import *
if __name__ == "__main__":
    EventUtils.seton('downloadlog')
    EventUtils.seton('networklog')
    EventUtils.seton('infolog')

    config.loadconfig()
    EventUtils.frun('loadqb', config['qbittorrent'])
    EventUtils.frun(eventname='loadbrowser', path=config['edge_exe_path'])
    BtHomeUtils.update_torrent(mode='drissionpage', mysqlconfig=config['mysql'])
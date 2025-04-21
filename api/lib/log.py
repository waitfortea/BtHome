from api.lib.ToolKits.log.logutils import *
from api.lib.ToolKits.event.evenutils import *
from api.lib.config import *
import os
import sys

@EventUtils.register('downloadlog')
def downloadlog(logdata, path=None):
    if path is None:
        path = f"{re.search(r'.*BtHome', os.path.dirname(__file__)).group()}/log/{config['logpath']['download_log_name']}"
    LogUtils.create(name='json').log(
        logpath=path
        , data=logdata)

@EventUtils.register('networklog')
def networklog(logdata, path=None):
    if path is None:
        path = f"{re.search(r'.*BtHome', os.path.dirname(__file__)).group()}/log/{config['logpath']['network_log_name']}"
    LogUtils.create(name='json')().log(
        logpath=path
        , data=logdata)

@EventUtils.register('infolog')
def infolog(logdata, path=None):
    if path is None:
        path = f"{re.search(r'.*BtHome', os.path.dirname(__file__)).group()}/log/{config['logpath']['info_log_name']}"
    LogUtils.create(name='info')().log(
        logpath=path
        , data=logdata)


if __name__ == "__main__":

    EventUtils.run(eventname='loadconfig')
    path1= f"{re.search(r'.*BtHome', os.path.dirname(__file__)).group()}/log/{config['logpath']['download_log_name']}"
    path2= f"{re.search(r'.*BtHome', os.path.dirname(__file__)).group()}/log/{config['logpath']['network_log_name']}"
    path3= f"{re.search(r'.*BtHome', os.path.dirname(__file__)).group()}/log/{config['logpath']['info_log_name']}"
    EventUtils.seton(eventname='downloadlog')
    EventUtils.run(eventname='infolog', logdata="sss", path=path3)


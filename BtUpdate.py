import sys

from api.lib.SubtitleGroupSubcribe import *
from api.lib.ToolKits.Strategy.AsyncStrategy import *
from api.lib.ToolKits.Proxy import *
from api.lib.Log import *
from api.lib.cfcheck import *
from api.lib.data_sql import *
setup_cfcheck()
setup_log()
setProxy()
setup_bthome_sql()
callEvent("bthome_sqlite_init")
callEvent("cf_check",{})

print("========开始更新:注意开启代理========")
asyncStrategy(update())
print("========更新结束:注意开启代理========")

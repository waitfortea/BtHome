import sys

from api.lib.SubtitleGroupSubcribe import *
from api.lib.ToolKits.Strategy.AsyncStrategy import *
from api.lib.ToolKits.Proxy import *
from api.lib.Log import *
from api.lib.cfcheck import *

setup_cfcheck()
setup_log()
setProxy()
callEvent("cf_check",{})

print("========开始更新:注意开启代理========")
asyncStrategy(update())
print("========更新结束:注意开启代理========")

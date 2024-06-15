
from api.lib.SubtitleGroupSubcribe import *
from api.lib.ToolKits.Strategy.AsyncStrategy import *
from api.lib.ToolKits.Proxy import *
from api.lib.Log import *

setup_log()
setProxy()
print("========开始更新:注意开启代理========")
asyncStrategy(update("迷宫饭"))
print("========更新结束:注意开启代理========")

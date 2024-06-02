from .FileProcess import *
from .CustomException import *
class LogProcessor:
    def __init__(self,logPath):
        self.init(logPath)

    def init(self,logPath):
        if isFile(logPath):
            self.logPath=pathInit(logPath,flag="file").absolutePath
            return
        raise InitFailedError(logPath)

    def append(self,message):
        with open(self.logPath,"a") as f:
            f.write(message)



from .FileProcess import *
class LogProcessor:
    def __init__(self,logPath):
        self.init(logPath)

    def init(self,logPath):
        if PathProcessor().isFile(logPath):
            self.logPath=PathProcessor.init(logPath).absolutePath
            return
        raise InitFailedError

    def append(self,message):
        with open(self.logPath,"a") as f:
            f.write(message)



from .FileProcess import *
class LogProcessor:
    def __init__(self,logPath):
        self.init(logPath)

    def init(self):
        if PathProcessor().isFile(self.logPath):
            self.logPath=PathProcessor.init(self.logPath).absolutePath

    def append(self,message):
        with open(self.logPath,"a") as f:
            f.write(message)


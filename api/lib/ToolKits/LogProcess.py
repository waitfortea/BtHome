from .FileProcess import *
from .CustomException import *
from dataclasses import dataclass
from datetime import datetime

class LogMessage:
    def __init__(self,data_dict):
        self.data=data_dict

    @property
    def datetime(self):
        timeStamp = datetime.now().strftime("%Y/%m/%d-%H:%M:%S")
        return timeStamp

    @property
    def message(self):
        data_text=""
        for key, value in self.data.items():
            data_text+=f"{key} :{value}\n"
        text=f"""\n======================================
{self.datetime}\n{data_text}======================================\n"""
        return text
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



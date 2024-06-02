import pickle
import os
from .FileProcess import *
from .CustomException import *
import yaml

class PickleProcessor:
    def __init__(self,savePath,obj=None):
        self.obj=obj
        self.savePath=savePath
        os.makedirs(os.path.dirname(self.savePath),exist_ok=True)

    def save(self):
        with open(self.savePath,'wb') as f:
            f.write(pickle.dumps(self.obj))

    def resotre(self):
        with open(self.savePath,'rb') as f:
            objText=f.read()
            return pickle.loads(objText)

class YamlProcessor:
    def __init__(self,filePath):
        self.init(filePath)
    def init(self,filePath):
        self.file=pathInit(filePath)
        if ".yaml" not in self.file.suffix:
            raise FileFormatNotAlign
    @property
    def contentDict(self):
        with open(self.file.absolutePath,'r') as f:
            content=yaml.safe_load(f)
        return content

if __name__=="__main__":
    yamlLoader=YamlProcessor("../config/config.yaml")
    print(yamlLoader.contentDict)
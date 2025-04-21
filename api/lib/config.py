from api.lib.ToolKits.parse.serializeutils import *
from api.lib.ToolKits.event.evenutils import *
import os
import sys
import json


class Config:
    _instance = None
    _initialized = False

    def __new__(cls,  config_dict=None, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, config_dict=None, *args, **kwargs):
        if not self._initialized:
            self.__class__._initialized = True
            self.config_dict = config_dict

    def __getitem__(self, item):
        return self.config_dict[item]

    def loadconfg(self, config_dict):
        self.config_dict = config_dict

    def __str__(self):
        return json.dumps(self.config_dict)

@EventUtils.register('loadconfig')
def loadconfig(path=f"{re.search(r'.*BtHome',os.path.dirname(__file__)).group()}/config/config.yaml"):
    global config
    config = config.loadconfg(SerializeUtils.get_yamldict(path))



config = Config()

if __name__ == "__main__":
    EventUtils.run('loadconfig')
    print(config)
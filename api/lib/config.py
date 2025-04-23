from api.lib.ToolKits.parse.serializeutils import *
from api.lib.ToolKits.event.evenutils import *
import os
import sys
import json


class Config(SerializeUtils):
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

    def loadconfig(self, path=None):
        if path is None:
            path = f"{re.search(r'.*BtHome', os.path.dirname(sys.argv[0])).group()}/config/config.yaml"

        self.config_dict = self.get_yamldict(path)

    def __str__(self):
        return json.dumps(self.config_dict)


config = Config()

if __name__ == "__main__":

    print(config)
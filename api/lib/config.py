from api.lib.ToolKits.parse.serializeutils import *
import os
import sys
print(sys.argv[0])
config = SerializeUtils.get_yamldict(f"{os.path.dirname(sys.argv[0])}/config/config.yaml")


def relaodConfig():
    global config
    config = SerializeUtils.get_yamldict(f"{os.path.dirname(sys.argv[0])}/config/config.yaml")



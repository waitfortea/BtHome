from api.lib.ToolKits.parseutils.serializeutils import *
import os
import sys
print(sys.argv[0])
configProcessor=YamlProcessor(f"{os.path.dirname(sys.argv[0])}/config/config.yaml")
config=configProcessor.contentDict

def relaodConfig():
    global config
    config=configProcessor.contentDict



from api.lib.ToolKits.SerializeProcessor import *
import os
import sys

configProcessor=YamlProcessor(f"{os.path.dirname(sys.argv[0])}/config/config.yaml")
config=configProcessor.contentDict

def relaodConfig():
    global config
    config=configProcessor.contentDict



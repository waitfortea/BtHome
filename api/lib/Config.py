from api.lib.ToolKits.SerializeProcessor import *
import os


configProcessor=YamlProcessor(f"{os.path.dirname(__file__)}/../../config/config.yaml")
config=configProcessor.contentDict


def relaodConfig():
    global config
    config=configProcessor.contentDict



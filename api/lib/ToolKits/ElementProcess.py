from dataclasses import dataclass
from lxml import etree
from .CustomType import *
from .CustomException import *
@dataclass
class ElementProcessor:
    def __init__(self,data):
        self.init(data)
    def init(self,data):
        self.element=""
        if Type(data).isStr:
            self.element=etree.HTML(data)
        if Type(data).type==etree._Element:
            self.element=data
        if self.element is None:
            raise InitFailedError

    def text(self):
        text_List=self.element.xpath(".//text()")
        return "".join(text_List) if text_List!=[] else ""

    def attrib(self,key):
        return self.element.attrib[key]

    def xpath(self,path):
        return [ElementProcessor(unit) for unit in self.element.xpath(path)]
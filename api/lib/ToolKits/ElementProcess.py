from dataclasses import dataclass
from lxml import etree

@dataclass
class ElementProcessor:
    element:etree.Element

    @property
    def text(self):
        try:
            text_List=self.element.xpath(".//text()")
            return "".join(text_List)

        except:
            print("元素无text属性")

    def attrib(self,key):
        return self.element.attrib[key]

    def xpath(self,xpath):
        return [ElementProcessor(element) for element in self.element.xpath(xpath)]
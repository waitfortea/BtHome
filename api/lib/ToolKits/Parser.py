from abc import ABC,abstractmethod
from Strategy import GeneralStrategy as GS
from lxml import etree
from dataclasses import dataclass
from lxml import etree
import ElementProcess as EP

@dataclass
class TextPather():
    htmlText:str
    xpath:str =None

@dataclass
class DomPather():
    dom:str
    xpath:str =None


class Parser(ABC):
    def __init__(self,Pather):
        self.Pather=Pather
    @abstractmethod
    def parse(self,ParseStrategy):
        pass

class DomParser(Parser):
    def parse(self,ParseStrategy):
        return ParseStrategy.execute(self.Pather)

    @property
    def dom(self):
        if 'dom' in dir(self.Pather):
            return EP.ElementProcessor(self.Pather.dom)
        else:
            return EP.ElementProcessor(etree.HTML(self.Pather.htmlText))

class ListElementStrategyByText(GS.Strategy):
    def execute(self,Pather):
        doc=etree.HTML(Pather.htmlText)

        elements_list=doc.xpath(Pather.xpath)
        EP_list=[EP.ElementProcessor(element) for element in elements_list]
        return  EP_list

class ListElementStrategyByDom(GS.Strategy):
    def execute(self,Pather):
        if isinstance(Pather.dom,EP.ElementProcessor):
            doc=Pather.dom.element
        else:
            doc=Pather.dom
        elements_list=doc.xpath(Pather.xpath)
        EP_list=[EP.ElementProcessor(element) for element in elements_list]

        return  EP_list




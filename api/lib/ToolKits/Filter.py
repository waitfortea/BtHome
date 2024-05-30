from dataclasses import dataclass
import numpy
import pandas
from abc import ABC,abstractmethod
from .Strategy import GeneralStrategy as GS
from dataclasses import dataclass

# @dataclass
# class FilterPather:
#     dataFrame:str
#     order_List:list=None
#     constrainStr_List:str=None
#     field:str=None
#
# class Filter(ABC):
#     def __init__(self,FilterPather):
#         self.FilterPather=FilterPather
#
#     @abstractmethod
#     def filter(self,FlterStrategy):
#        pass
#
# class DataFrameFilter(Filter):
#     def filter(self,FilterStrategy):
#         return FilterStrategy.execute(self.FilterPather)


class TitleFilterStrategyByOrder(GS.Strategy):
    def execute(self,FilterPather):
        return FilterPather.dataFrame.loc[FilterPather.order_List]


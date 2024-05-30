import pandas as pd
import numpy as np
from dataclasses import dataclass
from FileProcess import PathProcessor
from CustomException import *
from CustomType import Type

class ListProcessor:
    def __init__(self,list):
        if Type(list).isList:
            self.list=list
        else:
            raise TypeError

    @property
    def len(self):
        return len(self.list)

    def isLenAlign(self,compareList):
        if self.len==len(compareList):
            return True


    @property
    def isInerTypeAlign(self):
        if all(Type(i).isList for i in self.list):
            return True
        else:
            return False

    @property
    def isLenInnerAlign(self):
        if len(set([len(i) for i in self.list]))==1:
            return True
        else:
            return False

    @property
    def innerLen(self):
        if self.isLenInnerAlign:
            return len(self.list[0])
        else:
            raise LenAlignError


    @property
    def str_List(self):
        return [str(i) for i in self.list]

    @property
    def strip_List(self):
        return

    def converToMatchDict(self,value_List):
        if self.isLenAlign(value_List):
            match_Dict = {key: [] for key in set(self.list)}
            match_List = list(zip(self.list, value_List))
            for match in match_List:
                match_Dict[match[0]].append(match[1])
            return match_Dict
